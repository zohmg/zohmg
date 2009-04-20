package fm.last.darling;

import java.io.DataInput;
import java.io.IOException;
import java.util.Random;

import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.streaming.io.OutputReader;
import org.apache.hadoop.streaming.PipeMapRed;
import org.apache.hadoop.typedbytes.TypedBytesInput;
import org.apache.hadoop.typedbytes.TypedBytesWritable;


public class TableOutputReader extends OutputReader<ImmutableBytesWritable, BatchUpdate> {

	private ImmutableBytesWritable rowkey;
	private BatchUpdate batchupdate;

	private byte[] bytes;
	private DataInput clientIn;
	private TypedBytesWritable tbkey;
	private TypedBytesWritable tbvalue;
	private TypedBytesInput in;

	Random generator;

	@Override
	public void initialize(PipeMapRed pipeMapRed) throws IOException {
		super.initialize(pipeMapRed);

		rowkey = new ImmutableBytesWritable();
		batchupdate = new BatchUpdate();

		clientIn = pipeMapRed.getClientInput();
		tbkey = new TypedBytesWritable();
		tbvalue = new TypedBytesWritable();
		in = new TypedBytesInput(clientIn);
		generator = new Random();
	}

	@Override
	public boolean readKeyValue() throws IOException {
		System.err.println("readkey.");
		bytes = in.readRaw();
		if (bytes == null) {
			return false;
		}
		System.err.println("fine!");
		tbkey.set(bytes, 0, bytes.length);
		bytes = in.readRaw();
		tbvalue.set(bytes, 0, bytes.length);

		String rk = new Integer(generator.nextInt()).toString();
		String cfq = "ape:" + new Integer(generator.nextInt()).toString();
		byte[] value = new Integer(generator.nextInt()).toString().getBytes();

		rowkey = new ImmutableBytesWritable(rk.getBytes());
		batchupdate = new BatchUpdate(rk.getBytes());
		batchupdate.put(cfq, value);

		return true;
	}

	@Override
	public ImmutableBytesWritable getCurrentKey() throws IOException {
		return rowkey;
	}

	@Override
	public BatchUpdate getCurrentValue() throws IOException {
		return batchupdate;
	}

	@Override
	public String getLastOutput() {
		//return new TypedBytesWritable(bytes).toString();
		return new String("anything you want.");
	}

}
