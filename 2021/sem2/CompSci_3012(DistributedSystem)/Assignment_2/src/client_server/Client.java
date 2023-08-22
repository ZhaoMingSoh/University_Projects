package client_server;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.Namespace;
import org.jdom2.input.SAXBuilder;

import java.net.*;
import java.io.*;
import java.util.List;

public class Client {
    public static int lamport_clock = 1;
    public static int Get_Count = 0;

    public static void GET(Socket atom_Server, ObjectOutputStream atom_Out, int client_num){
        Get_Count++;
        String messageType = "GET";
        String start_line = "GET /atom.xml HTTP/1.1";
        String User_Agent = "ATOMClient/1/0";
        String host = String.valueOf(atom_Server.getLocalAddress());
        String Source = "Client";
        int source_num = client_num;
        String accept = "Accept: text/xml";
        Message wrapper = new Message(messageType, start_line, User_Agent, Source, source_num, host,0, Get_Count, accept);
        try {
            atom_Out.writeObject(wrapper);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Prints each of the Atom feed xml element into a text format
    public static void print_text(Element f_child){
        Namespace ns = Namespace.getNamespace("http://www.w3.org/2005/Atom");
        if(f_child.getName().equals("title")){
            System.out.println("title:"+f_child.getText());
        }else if(f_child.getName().equals("subtitle")){
            System.out.println("subtitle:"+f_child.getText());
        }else if(f_child.getName().equals("link")){
            System.out.println("link:"+f_child.getText());
        }else if(f_child.getName().equals("updated")){
            System.out.println("updated:"+f_child.getText());
        }else if(f_child.getName().equals("author")){
            System.out.println("author:"+f_child.getChild("name", ns).getText());
        }else if(f_child.getName().equals("id")) {
            System.out.println("id:" + f_child.getText());
        }else if(f_child.getName().equals("summary")){
            System.out.println("summary:" + f_child.getText());
        }
    }

    public static void Response_Handler(Message res_obj){
        String response_message = res_obj.get_message_content();
        System.out.println(response_message);

        try {
            SAXBuilder saxB = new SAXBuilder();
            String atom_xml_doc = res_obj.getAtom_xml_string();
            InputStream string_Stream = new ByteArrayInputStream(atom_xml_doc.getBytes("UTF-8"));
            Document atom_doc = saxB.build(string_Stream);
            Element root = atom_doc.getRootElement();
            List<Element> feeds =  root.getChildren();

            for(int i=0; i<feeds.size(); i++) {
                List<Element> feeds_child = feeds.get(i).getChildren();
                System.out.println(feeds.get(i).getName());
                for (int j = 0; j < feeds_child.size(); j++) {
                    if (!feeds_child.get(j).getName().equals("entry")) {
                        print_text(feeds_child.get(j));
                    } else if (feeds_child.get(j).getName().equals("entry")) {
                        System.out.println("entry");
                        List<Element> feeds_child_entry = feeds_child.get(j).getChildren();
                        for (int k = 0; k < feeds_child_entry.size(); k++) {
                            print_text(feeds_child_entry.get(k));
                        }
                    }
                }
                System.out.println();
            }
        }catch(JDOMException e){
            System.err.println();
            e.printStackTrace();
        }
        catch (IOException e){
            System.err.println();
            e.printStackTrace();
        }
    }

    public static void main(String[] args){
        String server_Name = args[0].substring(0,args[0].indexOf(':'));
        int port_Num = Integer.parseInt(args[0].substring(args[0].indexOf(':')+1));
        int client_num = Integer.parseInt(args[1]);

        try {
            Socket Atom_Server = new Socket(server_Name, port_Num);
            System.out.println("[Client] is connected to Atom Server.");
            ObjectOutputStream atom_out = new ObjectOutputStream(Atom_Server.getOutputStream());
            ObjectInputStream atom_in = new ObjectInputStream(Atom_Server.getInputStream());

            // GET() - request Aggregated Atom XML feed from the Atom Server
            GET(Atom_Server, atom_out, client_num);

            // response from the atom server
            Message res_Obj = (Message) atom_in.readObject();
            Response_Handler(res_Obj);

            Atom_Server.close();
        }catch (ClassNotFoundException e){
            e.printStackTrace();
        }catch (IOException e) {
            e.printStackTrace();
        }

    }
}
