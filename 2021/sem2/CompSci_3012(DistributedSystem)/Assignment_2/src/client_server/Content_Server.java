package client_server;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.Namespace;
import org.jdom2.output.Format;
import org.jdom2.output.XMLOutputter;

import java.io.*;
import java.net.Socket;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

public class Content_Server {
    public static int lamport_count = 1;
    public static int put_count = 0;
    public static boolean title_bool = false;
    public static boolean link_bool = false;
    public static boolean id_bool = false;
    public static Socket Atom_Server = null;

    public Content_Server(){
    }

    // Sends a PUT message alongside the input_?.xml file to the Atom Server
    public static void PUT(ObjectOutputStream atom_Out, String content, int input_num){
        put_count++; // counts the number of times PUT() is invoked
        lamport_count++;
        String messageType = "PUT";
        String start_line = "PUT /atom.xml HTTP/1.1";
        String user_Agent = "ATOMClient/1/0";
        String host = "Atom Server";
        String source = "Content Server";
        int source_num = input_num;
        String content_Type = "text/xml";

        File atom_xml_file = new File("./client_server/resources/input_"+input_num+".xml");
        Message wrapper = new Message(lamport_count, atom_xml_file, content,  messageType, start_line, user_Agent, host, 1, source, content_Type, (int) atom_xml_file.length(), source_num, put_count);
        try {
            atom_Out.writeObject(wrapper);
            atom_Out.flush();
            atom_Out.reset();
        } catch (IOException e) {
            System.err.println("[Content Server "+input_num+"] Error in writing an object to the Atom Server output stream.");
            e.printStackTrace();
        }
    }

    public static void response_Handler(Message response_Obj, ObjectOutputStream atom_out) throws IOException {
        // Perform lamport clock algorithm
        /*
            1. Take the larger clock between itself and the atom server.
            2. increment it by 1.
         */
        Lamport put_response_lamport = new Lamport(lamport_count, response_Obj.getLamport_clock());
        lamport_count = put_response_lamport.get_Lamport();

        // Print out the Atom Server's response to the recently sent PUT()
        String atom_Server_res = response_Obj.get_message_content();
        System.out.println(atom_Server_res);
    }

    public static String Atom_XML_Feed_Parser(String path, int input_num) throws IOException {
        // Atom XML feed converter
        boolean is_entry = false;
        ArrayList<Element> element_list = new ArrayList<>();

        // root element known the <feed>
        Namespace ns = Namespace.getNamespace("http://www.w3.org/2005/Atom");
        Element feed = new Element("Feed", ns);
        feed.setAttribute("lang", "en-US", Namespace.XML_NAMESPACE);

        Document doc = new Document(feed);

        File input = new File(path); // opens the input_?.txt file
        BufferedReader stream = new BufferedReader(new FileReader(input)); // place the input_?.txt file into the stream

        String line = stream.readLine();

        // Starts converting the input_?.txt contents format into ATOM XML feed format.
        /* (General Description) -
            1. identify the key ATOM elements from each line of inputs from the input_?.txt
            2. create an XML placeholder that contains the texts of each of the ATOM elements.
            3. append the XML placeholder to their relevant parent elements.
               a. if the key ATOM elements come after the "entry" element
                  then: append the key ATOM elements to the "entry" element (root -> entry -> others key ATOM elements)
                  else: append the key ATOM elements to the "feed" element (root -> others key ATOM elements)
         */
        String key = "";
        String text = "";

        // Checker to see if the required Atom Elements are present or not where each index represent an Atom Element
        Boolean[] atom_Elements = new Boolean[7];
        Arrays.fill(atom_Elements, false);
        int counter_ = -1;

        while (line != null) {
            if (line.equals("entry") == false) {
                String[] contents = line.split(":", 2);
                key = contents[0];
                text = contents[1];
            } else {
                key = line;
            }

            // Expected ATOM feed's elements
            if (key.equals("title")) {
                atom_Elements[0] = true;
                // Returns an error message for title that has no information
                if(text.isEmpty()){
                    title_bool = true;
                    System.err.println("[Content Server "+input_num+"] Input_"+input_num+".txt title field is empty. Please ensure that it is filled.");
                }
                // create the XML placeholder <title> for the ATOM element: title
                Element title = new Element("title", ns);
                // add the "texts" that follows the title to the placeholder <title>
                title.setText(text);
                /*
                    if the previous ATOM element is an "entry"
                    then: store all ATOM element to the element_list.
                    else: append the placeholder <title> to the root element <feed>
                 */
                if (!is_entry) {
                    doc.getRootElement().addContent(title);
                } else {
                    element_list.add(title);
                }
            } else if (key.equals("subtitle")) {
                atom_Elements[1] = true;
                Element subtitle = new Element("subtitle", ns);
                subtitle.setText(text);
                if (!is_entry) {
                    doc.getRootElement().addContent(subtitle);
                } else {
                    element_list.add(subtitle);
                }

            } else if (key.equals("link")) {
                atom_Elements[2] = true;
                // Returns an error message for link that has no information
                if(text.isEmpty()){
                    link_bool = true;
                    System.err.println("[Content Server "+input_num+"] Input_"+input_num+".txt link field is empty. Please ensure that it is filled.");
                }
                Element link = new Element("link", ns);
                link.setText(text);
                if (!is_entry) {
                    doc.getRootElement().addContent(link);
                } else {
                    element_list.add(link);
                }

            } else if (key.equals("updated")) {
                atom_Elements[3] = true;
                Element updated = new Element("updated", ns);
                updated.setText(text);
                if (!is_entry) {
                    doc.getRootElement().addContent(updated);
                } else {
                    element_list.add(updated);
                }
            } else if (key.equals("author")) {
                atom_Elements[4] = true;
                Element author = new Element("author", ns);
                Element name = new Element("name", ns);
                name.setText(text);
                author.addContent(name);
                if (!is_entry) {
                    doc.getRootElement().addContent(author);
                } else {
                    element_list.add(author);
                }
            } else if (key.equals("id")) {
                atom_Elements[5] = true;
                // Returns an error message for id that has no information
                if(text.isEmpty()){
                    id_bool = true;
                    System.err.println("[Content Server "+input_num+"] Input_"+input_num+".txt id field is empty. Please ensure that it is filled.");
                }
                Element id = new Element("id", ns);
                id.setText(text);
                if (!is_entry) {
                    doc.getRootElement().addContent(id);
                } else {
                    element_list.add(id);
                }
            } else if (key.equals("summary")) {
                atom_Elements[6] = true;
                Element summary = new Element("summary", ns);
                summary.setText(text);
                if (!is_entry) {
                    doc.getRootElement().addContent(summary);
                } else {
                    element_list.add(summary);
                }
            }

            counter_++;

            // Tells you how many atom elements are missing from the input_?.txt file by checking with the atom_Elements[]
//            if(atom_Elements[counter_] == false){
//                System.err.println("[Content Server "+input_num+"] Input_"+input_num+".txt is missing an Atom Elements.");
//            }

            // Ensure any subsequent ATOM elements that come after the "entry" element will be stored in the element_list
            if (key.equals("entry")) {
                counter_ = -1;
                // resets to check if the required Atom elements are present or not
                Arrays.fill(atom_Elements, false);
                is_entry = true;
                Element entry = new Element("entry", ns);
                // add the "entry" to the element list
                element_list.add(entry);
            }

            line = stream.readLine();
            if (line == null) {
                is_entry = false;
            }
        }

        // Append all the ATOM elements to the "entry" element that comes before them
            /* Ex:
                   element_list(entry, title, subtitle, ..., entry, title, subtitle, ...)
             */
        int counter = 0;
        int entry_num = 0;
        while (counter < element_list.size()) {
            if (element_list.get(counter).getName().equals("entry")) {
                entry_num = counter;
                doc.getRootElement().addContent(element_list.get(entry_num));
            } else {
                element_list.get(entry_num).addContent(element_list.get(counter));
            }
            counter++;
        }

        // Creates new input_?.xml files and stores the corresponding Atom Feed XML document into it
        XMLOutputter xmlOutput = new XMLOutputter();
        xmlOutput.setFormat(Format.getPrettyFormat());
        File atom_xml = new File("./client_server/resources/input_"+input_num+".xml");
        if(atom_xml.createNewFile()){
            System.out.println("[Content Server "+input_num+"] input_"+input_num+".xml is created from input_"+input_num+".txt.");
        }else{
            System.out.println("[Content Server "+input_num+"] input_"+input_num+".xml has already been created.");
        }
        xmlOutput.output(doc, new FileOutputStream(atom_xml));

        // Convert the input_?.xml files into strings to be sent over to the Atom Server
        String content = Files.readString(Paths.get(String.valueOf(atom_xml)), StandardCharsets.UTF_8);
        return content;
    }

    public static void main(String[] args){
        String server_Name = args[0].substring(0,args[0].indexOf(':'));
        int port_Num = Integer.parseInt(args[0].substring(args[0].indexOf(':')+1));
        String content = null;

        ObjectOutputStream atom_out = null;
        ObjectInputStream atom_in = null;

        // Create a socket that connects to the Atom Server host and its port
        try {
            Atom_Server = new Socket(server_Name, port_Num);
            System.out.println("[Content Server " + args[2] + "] is connected to Atom Server.");
        }catch (IOException e) {
            System.err.println("[Content Server " + args[2] + "] is unable to connect to Atom Server.");

        }

        try{
            atom_out = new ObjectOutputStream(Atom_Server.getOutputStream());
            atom_in = new ObjectInputStream(Atom_Server.getInputStream());
        }catch(IOException e) {
            System.err.println("[Content Server " + args[2] + "] cannot obtain the Atom Server input and output object streams.");
        }

        try{
            /*
                Converts Atom Key Elements in the Input_?.txt file to an Atom Feed XML document and stores it
                in input_?.xml file
             */
            try {
                content = Atom_XML_Feed_Parser(args[1], Integer.parseInt(args[2]));
            }catch(IOException e){
                System.err.println();
                e.printStackTrace();
            }

            // PUT() sends the input_?.xml (Atom Feed XML doc) to the Atom server
            PUT(atom_out, content, Integer.parseInt(args[2]));

            Content_Server_Handler alt_thread_server = new Content_Server_Handler(Atom_Server, port_Num, Integer.parseInt(args[2]), atom_out);
            alt_thread_server.start();

            // Communicates with the Atom Server
            Message res_Obj = null;
            while((res_Obj = (Message) atom_in.readObject()) != null) {
                response_Handler(res_Obj, atom_out); // response from the Atom Server
            }

//            Atom_Server.close();
        } catch (ClassNotFoundException e) {
            System.err.println("[Content Server " + args[2] + "] Message object's class is undefined.");
            e.printStackTrace();
        } catch (IOException e){
            System.err.println("[Content Server " + args[2] + "] is unable to read from and write to the Atom Server's object streams.");
            System.err.println();
        }finally {
            try {
                if (atom_out != null) {
                    atom_out.close();
                }
                if(atom_in != null){
                    atom_in.close();
                }
                Atom_Server.close();
            }catch(IOException e){
                e.printStackTrace();
            }
        }
    }

    public static class Content_Server_Handler extends Thread{
        public Socket atom_server = null;
        public int port = 0;
        public ObjectOutputStream atom_out = null;
        public int Content_Server_num = 0;
        public static int heartbeat_count = 0;

        public Content_Server_Handler(Socket atom_server, int port, int input_num, ObjectOutputStream atom_out){
            this.atom_server = atom_server;
            this.port = port;
            this.Content_Server_num = input_num;
            this.atom_out = atom_out;
        }

        public void run(){
            while(true){
                try {
                    heartbeat_count++;
                    Thread.sleep(12*1000);
                    String messageType = "Heartbeat";
                    String startLine = "Content Server "+Content_Server_num+": I Am Alive.";
                    String userAgent = "ATOMClient/1/0";
                    String host = "Atom Server";
                    String source = "Content Server";
                    int source_num = Content_Server_num;
                    Message heartbeat = new Message(0, null, null, messageType, startLine, userAgent, host, 1, source, null, 0, source_num, heartbeat_count);
                    try {
                        atom_out.writeObject(heartbeat);
                        atom_out.flush();
                        atom_out.reset();
                    }catch (SocketException e) {
//
                        System.err.println("[Content Server " + Content_Server_num + "] has disconnected from the Atom Server.");
                        int retry_connect_count = 0;
                        while (retry_connect_count < 3) {
                            retry_connect_count++;
                            connect_to_Server(atom_server, port);

                        }
                        e.printStackTrace();
                        break;
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (IOException e){
                    e.printStackTrace();
                }
            }
        }

        private void connect_to_Server(Socket atom_server, int port) {

        }
    }
}
