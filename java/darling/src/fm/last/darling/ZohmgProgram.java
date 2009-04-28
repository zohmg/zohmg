package fm.last.darling;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.io.RowResult;
import org.apache.hadoop.hbase.mapred.TableOutputFormat;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.JobPriority;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.lib.LongSumReducer;

import fm.last.darling.io.records.NSpacePoint;
import fm.last.darling.mapred.MapperWrapper;
import fm.last.darling.mapred.ZohmgCombiner;
import fm.last.darling.mapred.ZohmgReducer;


public class ZohmgProgram {
	public static final JobPriority DEFAULT_JOB_PRIORITY = JobPriority.NORMAL;

	public void start(String input) throws Exception {
		Path path = new Path(input);

		// TODO: read table/dataset from environment.
		String table = "zohmg";

	    JobConf job = new JobConf(ZohmgProgram.class);
	    job.setJobName("zohmg!");
	    job.setJobPriority(DEFAULT_JOB_PRIORITY);
	    FileInputFormat.addInputPath(job, path);

	    Path output = new Path("yeah");
	    FileOutputFormat.setOutputPath(job, output);

	    // input
		job.setInputFormat(TextInputFormat.class);
		// wrapper
		job.setMapperClass(MapperWrapper.class);
		job.setMapOutputKeyClass(NSpacePoint.class);
		job.setMapOutputValueClass(IntWritable.class);
		// output
	    job.setCombinerClass(ZohmgCombiner.class);
	    job.setReducerClass(ZohmgReducer.class);
		job.setOutputFormat(TableOutputFormat.class);
		job.setOutputKeyClass(ImmutableBytesWritable.class);
		job.setOutputValueClass(BatchUpdate.class);
		job.set(TableOutputFormat.OUTPUT_TABLE, table);

	    JobClient.runJob(job);
	}
}
