package fm.last.darling.mapred;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;

import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;

import fm.last.darling.hbase.HBaseUtils;
import fm.last.darling.io.records.NSpacePoint;
import fm.last.darling.nspace.Projection;

public class ZohmgReducer extends MapReduceBase implements Reducer<NSpacePoint, IntWritable, ImmutableBytesWritable, BatchUpdate> {
	public void reduce(NSpacePoint point, Iterator<IntWritable> values, OutputCollector<ImmutableBytesWritable, BatchUpdate> output, Reporter reporter) throws IOException {
		// sum the values.
		int sum = 0;
        while (values.hasNext())
            sum += values.next().get();

        byte[] n = new Integer(sum).toString().getBytes();
        // or, if you'd rather like to store byte-y ints:
        //byte[] n = Util.intToByteArray(sum);

        // HBase stuff.
        byte[] rowkey = HBaseUtils.formatRowkey(point.getUnit(), point.getTimestamp());
        ImmutableBytesWritable rk = new ImmutableBytesWritable(rowkey);
        BatchUpdate update        = new BatchUpdate(rowkey);

        Projection p = new Projection(point);
        update.put(p.toHBaseCFQ(), n);
        // dispatch to HBase.
        output.collect(rk, update);
	}
}
