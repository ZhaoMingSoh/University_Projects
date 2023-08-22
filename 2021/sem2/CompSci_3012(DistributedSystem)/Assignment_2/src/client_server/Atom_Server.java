package client_server;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.Namespace;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.Format;
import org.jdom2.output.XMLOutputter;

import java.net.ServerSocket;

import java.net.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Atom_Server {
    public static int lamport_clock = 1;
    public static int counter = 0;
    public static int response_count = 0;
    public static final int Port_Num = 9090;
    public static Map<String, ArrayList<Object>> c_mapper = new LinkedHashMap<>();

    public Atom_Server(){
        counter++;
    }

    public static void create_Atom_XML(){
        try {
            // Create a new local file to store the Atom XML Feed
            File aggregated_feed = new File("./client_server/atom_resources/aggregated.xml");
            if (aggregated_feed.createNewFile()) {
                System.out.println("[Atom Server] File is created: aggregated.xml");
            } else {
                System.out.println("[Atom Server] File already existed: aggregated.xml");
            }

            //Pretty formatter for the Atom xml Feed
            XMLOutputter xmlOutput = new XMLOutputter();
            xmlOutput.setFormat(Format.getPrettyFormat());
            SAXBuilder dom_Builder = new SAXBuilder();

            // Create a new Atom XML document
            Namespace ns = Namespace.getNamespace("http://www.w3.org/2005/Atom");
            Element newRoot = new Element("Feed", ns);
            newRoot.setAttribute("lang", "en-US", Namespace.XML_NAMESPACE);
            Document newDoc = new Document(newRoot);

            // Iterate through the map and append each of the content server's "input_?.xml" into the "aggregated.xml"
            Iterator<String> iterator = c_mapper.keySet().iterator(); // returns an iterator from cs_mapper
            while (iterator.hasNext()) {
                String key = iterator.next();
                System.out.println(key);
                ArrayList<Object> values = new ArrayList<>(c_mapper.get(key));
                String content = (String) values.get(2);
                InputStream string_Stream = new ByteArrayInputStream(content.getBytes("UTF-8")); // read the string into an InputStream
                Document atom_doc = dom_Builder.build(string_Stream);
                Element root = atom_doc.detachRootElement();
                root.removeAttribute("lang", Namespace.XML_NAMESPACE);
                newRoot.addContent(root.clone());

            }
            // Store the corresponding Document object into the aggregated.xml file
            xmlOutput.output(newDoc, new FileOutputStream(aggregated_feed));

        }catch(IOException | JDOMException e){
            e.printStackTrace();
        }


    }

    public static void Handle_PUT(Message client_Obj, String thread_name){
         /*
            Update Atom_Server Lamport Clock - Choose the larger clock between the Content ? server and Atom Server and increment by 1
         */
        Lamport put_update = new Lamport(lamport_clock, client_Obj.getLamport_clock());
        lamport_clock = put_update.get_Lamport();

        // Display the client message in the Atom Server interface
        String client_Message = client_Obj.get_message_content();
        System.out.println(client_Message);

        // Prints out the Atom XML Feed into the Atom Server interface
        String atom_xml_feed_string = client_Obj.getAtom_xml_string();
        System.out.println(atom_xml_feed_string);

        ArrayList<Object> first = new ArrayList<>();
        first.add(client_Obj.get_Client_Type());
        first.add(client_Obj.get_Source_num());
        first.add(atom_xml_feed_string);
        c_mapper.put(thread_name,first);

    }

    public static void Handle_GET(Message client_Obj){
        // Display the client message in the Atom Server interface
        String client_Message = client_Obj.get_message_content();
        System.out.println(client_Message);
    }

    public static void Server_Response(Message client_Obj, ObjectOutputStream c_Out){
        response_count++;
        lamport_clock++;
        String messageType = client_Obj.get_Message_Type();
        String start_Line = "";

        // Which client are you sending the response back to ?
        String host = client_Obj.get_Client_Type(); // Content Server or Client
        int host_num = client_Obj.get_Source_num();
        System.out.println(host_num);

        // Who is the sender of this response ?
        String source = "Atom Server";
        int source_num = counter; // Atom server's number
        String xml_doc = null;

        // Response to the PUT() from the Content Server
        if(host.equals("Content Server")) {
            xml_doc = client_Obj.getAtom_xml_string();
            if(xml_doc.isEmpty() == false){
                if(client_Obj.get_Label() <= 1) {
                    start_Line = "HTTP/1.1 201 ATOM_FEED_CREATED";
                }else{
                    start_Line = "HTTP/1.1 200 OK";
                }
            }else{
                start_Line = "HTTP/1.1 204 NO CONTENT";
            }
        }

        // Response to the GET() from the Client
        if(host.equals("Client")){
            start_Line = "HTTP/1.1 200 OK";
            System.out.println(host_num);
            try {
                xml_doc = Files.readString(Paths.get("./client_server/atom_resources/aggregated.xml"), StandardCharsets.UTF_8);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        String content_Type = "text/xml";
        int content_Length = xml_doc.length();
        Message res = new Message(lamport_clock, messageType+" response", start_Line, host, host_num, source, source_num , content_Type, content_Length, null, xml_doc, response_count);

        try {
            c_Out.writeObject(res);
            c_Out.flush();
            c_Out.reset();
        } catch (IOException e) {
            System.err.println("[Atom Server] Error in sending the response object back to the requesting client !!");
            e.printStackTrace();
        }
    }

    public static void main(String[] args){
        try {
            Atom_Server inc = new Atom_Server();
            ServerSocket atom_Server = new ServerSocket(Port_Num);
            System.out.println("[Atom Server] is running ......");
            while(true) {
                System.out.println("[Atom Server] is waiting for client's connection request ......");
                Socket client = atom_Server.accept();
                System.out.println("[Atom Server] is connected to a client.");
                Client_Handler new_Client = new Client_Handler(client, c_mapper);
                new_Client.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static class Client_Handler extends Thread{
        private Socket client_Socket;
        private Map<String, ArrayList<Object>> c_mapper;
        private ObjectInputStream c_In;
        private ObjectOutputStream c_Out;

        public Client_Handler(Socket client_Socket, Map<String, ArrayList<Object>> c_mapper) {
            this.c_mapper = c_mapper;
            this.client_Socket = client_Socket;
        }


        public void run(){
            try {
                c_Out = new ObjectOutputStream(client_Socket.getOutputStream());
                c_In = new ObjectInputStream(client_Socket.getInputStream());
            }catch(IOException e) {
                System.err.println("[Atom Server "+counter+" ] Error in obtaining the client's input and output object streams.");
                e.printStackTrace();
            }

            // The Atom server is always waiting for client operations/requests to continue its execution ...
            while (true) {
                Message client_Obj = null;
                try {
                    client_Obj = (Message) c_In.readObject();
                    String requested_operations = client_Obj.get_Message_Type();
                    if (requested_operations.equals("PUT")) { // Put operation from the Content Server
                        System.out.println("--------------[PUT Operation]-----------------");
                        Handle_PUT(client_Obj, currentThread().getName());
                        Server_Response(client_Obj, c_Out);
                        System.out.println("----------------------------------------------");
                    } else if (requested_operations.equals("GET")) { // Get operation from the Client
                        System.out.println("--------------[GET Operation]-----------------");
                        Handle_GET(client_Obj);
                        create_Atom_XML();
                        Server_Response(client_Obj, c_Out);
                        System.out.println("----------------------------------------------");
                    }else if(requested_operations.equals("Heartbeat")){
                        System.out.println("--------------[Heartbeat Operation]-----------------");
                        System.out.println(client_Obj.get_message_content());
                        System.out.println("----------------------------------------------");
                    }
                }catch(EOFException e){
                    // Remove content server that is no longer connecting with teh Atom Server
                    if(c_mapper.containsKey(currentThread().getName())){
                        System.out.println("--------------[Disconnection]-----------------");
                        String content_name_num = (String)c_mapper.get(currentThread().getName()).get(0) + " " +String.valueOf((int)c_mapper.get(currentThread().getName()).get(1));
                        System.out.println("[Atom Server"+counter+"] "+content_name_num+" has died.");
                        c_mapper.remove(currentThread().getName());
                        System.out.println("----------------------------------------------");
                    }
                    break;
                    /*
                        Deal with the Expected behaviour of the c_In as the client ObjectInputStream
                        will not have any bytes coming from the client after the client has correctly
                        received the aggregated.xml file
                     */
                }catch(IOException e) {
                    System.err.println("[Atom Server "+counter+" ] Error in reading and writing to input and output object streams.");
                    e.printStackTrace();
                }catch (ClassNotFoundException e) {
                    System.err.println("[Atom Server "+counter+" ] The Message object's class is undefined.");
                    e.printStackTrace();
                }
            }
        }
    }
}


