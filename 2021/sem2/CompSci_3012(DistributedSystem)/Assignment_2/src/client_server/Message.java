package client_server;

import java.io.File;
import java.io.Serializable;

public class Message implements Serializable {
    private int lamport_clock;
    private File atom_xml;
    private String atom_xml_string;
    private String message_Type;
    private String start_Line;
    private String user_Agent;
    private String host;
    private int host_num;
    private String source;
    private int source_num;
    private String content_Type;
    private int content_Size;
    private int Operation_label;
    private String Accept;


    // Content server overloaded constructor
    public Message(int lamport_clock, File atom_xml, String atom_xml_string, String message_Type, String start_Line, String user_Agent, String host, int host_num, String source, String content_Type, int content_Size, int source_num, int label){
        this.lamport_clock = lamport_clock;
        this.atom_xml = atom_xml;
        this.atom_xml_string = atom_xml_string;
        this.message_Type = message_Type;
        this.start_Line = start_Line;
        this.user_Agent = user_Agent;
        this.host = host;
        this.host_num = 0;
        this.source = source;
        this.source_num = source_num;
        this.content_Type = content_Type;
        this.content_Size = content_Size;
        this.Operation_label = label;
        this.Accept = "";
    }

    // client overload constructor
    public Message(String message_Type, String start_Line, String user_Agent, String source, int source_num, String host, int host_num, int label, String Accept){
        this.atom_xml = null;
        this.message_Type = message_Type;
        this.start_Line = start_Line;
        this.user_Agent = user_Agent;
        this.host = host;
        this.host_num = host_num;
        this.source = source;
        this.source_num = source_num;
        this.content_Type = "";
        this.content_Size = 0;
        this.Operation_label = label;
        this.Accept = Accept;
    }

    // Atom Server "response" overloaded constructor
    public Message(int lamport_clock, String message_Type, String start_Line, String host, int host_num, String source, int source_num, String content_Type, int content_Size, File atom_File, String atom_xml_string, int label){
        this.lamport_clock = lamport_clock;
        this.atom_xml = atom_File;
        this.atom_xml_string = atom_xml_string;
        this.message_Type = message_Type;
        this.start_Line = start_Line;
        this.user_Agent = "";
        this.host = host;
        this.host_num = host_num;
        this.source = source;
        this.source_num = source_num;
        this.content_Type = content_Type;
        this.content_Size = content_Size;
        this.Operation_label = label;
        this.Accept = "";
    }

    String get_message_content(){
        String message = "";

        // GET message from Client
        if(source.equals("Client")){
            message = start_Line+"\n"+
                    "User-Agent: "+user_Agent+"\n"+
                    "Host: "+host+"\n"+
                    "Source: "+source+" "+source_num+"\n";
        }else if(source.equals("Content Server")){ // PUT message from Content Server
            if(Operation_label <= 1 && message_Type.equals("PUT")) { // The first PUT message from CS --> AS
                message = "Lamport-Clock: "+ lamport_clock +"\n"+
                        start_Line + "\n" +
                        "User-Agent: " + user_Agent + "\n" +
                        "Host: " + host + "\n" +
                        "Source: " + source + " " + source_num + "\n"
                        + "Content-Type: " + content_Type + "\n" +
                        "Content-Size: " + content_Size + "\n";
            }
            if(Operation_label > 1 && message_Type.equals("PUT")){ // The subsequent PUT message from CS --> AS
                message ="Lamport-Clock: "+ lamport_clock +"\n"+
                        start_Line + "\n" +
                        "User-Agent: " + user_Agent + "\n" +
                        "Host: " + host +" "+ host_num + "\n" +
                        "Source: " + source + " " + source_num + "\n"
                        + "Content-Type: " + content_Type + "\n" +
                        "Content-Size: " + content_Size + "\n";
            }
            if(message_Type.equals("Heartbeat")){
                message = start_Line + "\n" +
                        "User-Agent: " + user_Agent + "\n" +
                        "Host: " + host +" "+ host_num + "\n" +
                        "Source: " + source + " " + source_num + "\n";
            }
        }else if(source.equals("Atom Server")){ // Response from the Atom Server
            message = "Lamport-Clock: "+ lamport_clock +"\n"+
                    start_Line + "\n" +
                    "Host: " + host +" "+ host_num + "\n" +
                    "Source: " + source + " " + source_num + "\n" +
                    "Content-Type: " + content_Type + "\n" +
                    "Content-Size: " + content_Size + "\n";
        }
        return message;
    }

    File get_Atom_Doc(){
        return atom_xml;
    }

    String getAtom_xml_string(){
        return atom_xml_string;
    }

    int getLamport_clock(){
        return lamport_clock;
    }

    String get_Message_Type(){
        return message_Type;
    }

    String get_Msg_Status_Code(){
        return start_Line.substring(start_Line.indexOf(" ")+1);
    }

    String get_Client_Type(){
        return source;
    }

    String get_Start_Line(){
        return start_Line;
    }

    int get_Source_num(){
        return source_num;
    }

    int get_Label(){
        return Operation_label;
    }
}
