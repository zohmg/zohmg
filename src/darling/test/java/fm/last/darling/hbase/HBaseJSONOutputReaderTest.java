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

public class HBaseJSONOutputReaderTest {

  String keyString1 = "pageviews-20080717";
  String column1 = "country-domain-useragent-usertype:all-m.last.fm-other-all";
  
  String keyString2 = "pageviews-20090101";
  String column2 = "country:all";
  
  @Test
  public void test() throws IOException {
    PipeReducer pipeReducer = new MockPipeReducer();
    pipeReducer.configure(new JobConf());

    HBaseJSONOutputReader outputReader = new HBaseJSONOutputReader();
    outputReader.initialize(pipeReducer);

    assertTrue(outputReader.readKeyValue());

    //first key value
    ImmutableBytesWritable expectedKey1 = new ImmutableBytesWritable(keyString1.getBytes("UTF-8"));
    assertEquals(expectedKey1, outputReader.getCurrentKey());
    
    BatchUpdate expectedValue1 = new BatchUpdate(keyString1);
    expectedValue1.put(column1, new byte[] {49, 57});
    assertEquals(0, expectedValue1.compareTo(outputReader.getCurrentValue())); //no equals

    
    assertTrue(outputReader.readKeyValue());
    
    //second one
    ImmutableBytesWritable expectedKey2 = new ImmutableBytesWritable(keyString2.getBytes("UTF-8"));
    assertEquals(expectedKey2, outputReader.getCurrentKey());
    
    BatchUpdate expectedValue2 = new BatchUpdate(keyString2);
    expectedValue2.put(column2, new byte[] {49, 57});
    assertEquals(0, expectedValue2.compareTo(outputReader.getCurrentValue())); //no equals

    
    assertFalse(outputReader.readKeyValue());
  }

  class MockPipeReducer extends PipeReducer {

    String input1 = "'" + keyString1 + "'\t'{\""+ column1 + "\": {\"value\": 19}}'";
    String input2 = "'" + keyString2 + "'\t'{\""+ column2 + "\": {\"value\": 19}}'";
    byte[] inpututf8;

    public MockPipeReducer() throws UnsupportedEncodingException {
      inpututf8 = (input1 + "\n" + input2).getBytes("UTF-8");
    }

    @Override
    public DataInput getClientInput() {
      return new DataInputStream(new ByteArrayInputStream(inpututf8));
    }
  }

}
