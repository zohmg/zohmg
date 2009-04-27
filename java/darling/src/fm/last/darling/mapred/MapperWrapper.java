package fm.last.darling.mapred;

import java.io.IOException;
import java.util.Iterator;
import java.util.Map;

import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import fm.last.darling.user.UserMapper;
import fm.last.darling.user.ExampleMapper;


// the class we wrap around the user's mapper.
public class MapperWrapper implements Mapper<LongWritable, Text, ImmutableBytesWritable, BatchUpdate> {
	private UserMapper usermapper;

	public MapperWrapper() throws Exception {
		// read name of user's mapper class from config.

		// dynamically instantiate user's class.
		String userclass = "fm.last.darling.user.ExampleMapper";
		try {
			usermapper = (UserMapper) Class.forName(userclass).newInstance();
		} catch(Exception e) {
			System.err.println("could not instantiate userclass.");
			throw new IOException("total instantiation fail.");
		}
	}
	
	public void close() throws IOException {}
	public void configure(JobConf conf) {}

	public void map(LongWritable key, Text value, OutputCollector<ImmutableBytesWritable, BatchUpdate> collector, Reporter reporter) throws IOException {
		ZohmgOutputCollector o = new ZohmgOutputCollector();
		// call on user's mapper
		usermapper.map(key.toString(), value.toString(), o);
		
		// perform dimensionality reduction,
		
		// and collect.
		
	}
	
	public static void main(String[] args) throws Exception {
		System.out.println("yeah, that's right.");
		LongWritable k = new LongWritable(42);
		Text v = new Text("from nowhere.");

		ZohmgOutputCollector o = new ZohmgOutputCollector();
		
		String userclass = "fm.last.darling.user.ExampleMapper";
		UserMapper usermapper = (UserMapper) Class.forName(userclass).newInstance();
		//UserMapper usermapper = new ExampleMapper();		
		
		usermapper.map("random-key", "123423423	SE	web	510", o);
		
		Map<String, String> d = o.getDimensions();
		Iterator<Map.Entry<String, String>> i = d.entrySet().iterator();
		while (i.hasNext()) {
			Map.Entry<String, String> e = i.next();
			String key = e.getKey();
			String val = e.getValue();
			System.out.println("k, v: " + key + " & " + val);
			
		}
	}
}
