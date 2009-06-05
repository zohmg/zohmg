package fm.last.darling.hbase;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.ByteArrayInputStream;
import java.io.DataInput;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.streaming.PipeReducer;
import org.junit.Test;

import fm.last.darling.hbase.HBaseJSONOutputReader;

public class HBaseTypedBytesOutputReaderTest {

  byte[] key1 = new byte[] {};
  byte[] column1 = new byte[] {};
  
  byte[] key2 = new byte[] {};
  byte[] column2 = new byte[] {};
  
  @Test
  public void test() throws IOException {
    PipeReducer pipeReducer = new MockPipeReducer();
    pipeReducer.configure(new JobConf());

    HBaseTypedBytesOutputReader outputReader = new HBaseTypedBytesOutputReader();
    outputReader.initialize(pipeReducer);

    assertTrue(outputReader.readKeyValue());

    //first key value
    ImmutableBytesWritable expectedKey1 = new ImmutableBytesWritable(key1);
    assertEquals(expectedKey1, outputReader.getCurrentKey());
    
    BatchUpdate expectedValue1 = new BatchUpdate(key1);
    expectedValue1.put(column1, new byte[] {49, 57});
    assertEquals(0, expectedValue1.compareTo(outputReader.getCurrentValue())); //no equals

    
    assertTrue(outputReader.readKeyValue());
    
    //second one
    ImmutableBytesWritable expectedKey2 = new ImmutableBytesWritable(key2);
    assertEquals(expectedKey2, outputReader.getCurrentKey());
    
    BatchUpdate expectedValue2 = new BatchUpdate(key2);
    expectedValue2.put(column2, new byte[] {49, 57});
    assertEquals(0, expectedValue2.compareTo(outputReader.getCurrentValue())); //no equals

    
    assertFalse(outputReader.readKeyValue());
  }

  class MockPipeReducer extends PipeReducer {

    byte[] input; //TODO set something!!

    public MockPipeReducer() throws UnsupportedEncodingException {
      input = new byte[] {}
    }

    @Override
    public DataInput getClientInput() {
      return new DataInputStream(new ByteArrayInputStream(input));
    }
  }

}
