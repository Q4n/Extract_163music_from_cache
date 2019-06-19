package process;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.ArrayList;

/**
 * 
 * @author Q4n
 *
 *		MusicUnpack[] ps=new MusicUnpack[10];
		for(int i=0;i<ps.length;i++){
			ps[i]=new MusicUnpack("D:\\Cpp");
		}
		for(MusicUnpack i:ps){
			i.start();
		}
		for(MusicUnpack i:ps){
			i.join();
		}
		System.out.println("All done!");
 */
public class MusicUnpack extends Thread{
	private static ArrayList<String> paths;
	public MusicUnpack(String path) {
		// TODO Auto-generated constructor stub
		paths=new ArrayList<String>();
		travelPath(path);
		if(paths.isEmpty()){
			System.out.println("Path is empty!");
		}
	}
	private void travelPath(String path){
		File file=new File(path);
		if(file.exists()){
			File[] files=file.listFiles();
			if(files==null||files.length==0){
				return;
			}
			else{
				for(File i:files){
					if(i.isDirectory()){
						travelPath(i.getAbsolutePath());
					}
					else{
						if(i.getName().substring(i.getName().lastIndexOf('.')).equals(".uc"))
							paths.add(i.getAbsolutePath());
					}
				}
			}
		}else{
			System.out.println("Path is not exist!");
		}
	}
	private void unpack(String filename){
		try {
			File file=new File(filename);
			FileInputStream fileInputStream=new FileInputStream(file);
			FileOutputStream fileOutputStream=new FileOutputStream(new File(filename+".mp3"));
			int flag;
			byte[] tmpbyte = new byte[1024];
			byte[] resbyte=new byte[1024];
			while((flag=fileInputStream.read(tmpbyte))!=-1){
				for(int i=0;i<tmpbyte.length;i++){
					resbyte[i]=(byte) (tmpbyte[i]^163);
				}
				fileOutputStream.write(resbyte);
			}
			fileInputStream.close();
			fileOutputStream.close();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	public void run() {
		while(!paths.isEmpty()){
			String thisfile=paths.remove(0);
			unpack(thisfile);
		}
	};
}
