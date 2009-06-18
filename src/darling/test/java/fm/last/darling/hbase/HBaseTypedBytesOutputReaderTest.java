package fm.last.darling.hbase;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInput;
import java.io.DataInputStream;
import java.io.DataOutput;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.streaming.PipeReducer;
import org.apache.hadoop.typedbytes.TypedBytesOutput;
import org.junit.Test;

public class HBaseTypedBytesOutputReaderTest {
  
  @Test
  public void test() throws IOException {
    PipeReducer pipeReducer = new MockPipeReducer();

    HBaseTypedBytesOutputReader outputReader = new HBaseTypedBytesOutputReader();
    outputReader.initialize(pipeReducer);

    assertTrue(outputReader.readKeyValue());
    // key
    ImmutableBytesWritable expectedKey1 = new ImmutableBytesWritable("artist-1000-track-200-20090618".getBytes());
    assertEquals(expectedKey1, outputReader.getCurrentKey());
    // value
    Put expectedValue1 = new Put("artist-1000-track-200-20090618".getBytes());
    expectedValue1.add("unit".getBytes(), "scrobbles".getBytes(), new byte[] {10});
    assertEquals(0, expectedValue1.compareTo(outputReader.getCurrentValue()));

    // that would be all, thank you.
    assertFalse(outputReader.readKeyValue());
  }

  class MockPipeReducer extends PipeReducer {

	  TypedBytesOutput tbout; // sink.
	  ByteArrayOutputStream baos;

	  public MockPipeReducer() throws UnsupportedEncodingException {
		  baos = new ByteArrayOutputStream();
		  DataOutput out = new DataOutputStream(baos);
		  tbout = new TypedBytesOutput(out);

		  try {
			  write_data();
		  } catch (IOException e) {
			  System.err.println("write failed.");
		  }
	  }

	  // simulates output from mapred job.
	  private void write_data() throws IOException {
		  // key
		  String key = new String("artist-1000-track-200-20090618");
		  tbout.write(key);
		  // and value - always a map.
		  Map<String, Integer> m = new HashMap<String, Integer>();
		  m.put("unit:scrobbles", 10);
		  m.put("unit:loves", 2);
		  tbout.write(m);
	  }

    @Override
    public DataInput getClientInput() {
    	return new DataInputStream(new ByteArrayInputStream(baos.toByteArray()));
    }
  }

}
