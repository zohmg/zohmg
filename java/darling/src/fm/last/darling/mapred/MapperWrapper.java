package fm.last.darling.mapred;

import java.io.IOException;

import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

// the class we wrap around the user's mapper.
public class MapperWrapper implements Mapper<LongWritable, Text, ImmutableBytesWritable, BatchUpdate> {
	private Mapper usermapper;

	public MapperWrapper() {
		// read name of user's mapper class from config.
		// dynamically instantiate user's class.
		//usermapper = new  
	}
	
	public void close() throws IOException {}
	public void configure(JobConf conf) {}

	public void map(LongWritable key, Text value, OutputCollector<ImmutableBytesWritable, BatchUpdate> collector, Reporter reporter) throws IOException {
		// call on user's mapper.
		
		
		// perform dimensionality reduction.
		
	}
}
