package fm.last.darling.mapred;

import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;

import fm.last.darling.io.records.NSpacePoint;

public class ZohmgCombiner extends MapReduceBase implements Reducer <NSpacePoint, IntWritable, NSpacePoint, IntWritable> {
	public void reduce(NSpacePoint k, Iterator<IntWritable> values, OutputCollector<NSpacePoint, IntWritable> output, Reporter reporter) throws IOException {
		int sum = 0;
        while (values.hasNext())
            sum += values.next().get();
        output.collect(k, new IntWritable(sum));
	}
}
