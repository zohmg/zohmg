package fm.last.darling;

import java.io.DataInput;
import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.streaming.io.OutputReader;
import org.apache.hadoop.streaming.PipeMapRed;
import org.apache.hadoop.typedbytes.TypedBytesInput;
import org.apache.hadoop.typedbytes.TypedBytesWritable;
import java.io.DataInput;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.nio.charset.CharacterCodingException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.streaming.PipeMapRed;
import org.apache.hadoop.streaming.StreamKeyValUtil;
import org.apache.hadoop.streaming.io.OutputReader;
import org.apache.hadoop.util.LineReader;
import org.apache.hadoop.util.StringUtils;
import org.apache.hadoop.util.UTF8ByteArrayUtils;
import java.util.Random;


public class TBOutputReader extends OutputReader<Text, Text> {

	  private byte[] bytes;
	  private DataInput clientIn;
	  private TypedBytesWritable tbkey;
	  private TypedBytesWritable tbvalue;
	  private TypedBytesInput in;
	
	  @Override
	  public void initialize(PipeMapRed pipeMapRed) throws IOException {
	    super.initialize(pipeMapRed);
	    clientIn = pipeMapRed.getClientInput();
	    tbkey = new TypedBytesWritable();
	    tbvalue = new TypedBytesWritable();
	    in = new TypedBytesInput(clientIn);
	  }
	
	  @Override
	  public boolean readKeyValue() throws IOException {
	    bytes = in.readRaw();
	    if (bytes == null) {
	      return false;
	    }
	    tbkey.set(bytes, 0, bytes.length);
	    bytes = in.readRaw();
	    tbvalue.set(bytes, 0, bytes.length);
	    return true;
	  }
	
	  @Override
	  public Text getCurrentKey() throws IOException {
	    return new Text(tbkey.toString());
	  }
	
	  @Override
	  public Text getCurrentValue() throws IOException {
		  return new Text(tbvalue.toString());
	  }

	  @Override
	  public String getLastOutput() {
	    return new TypedBytesWritable(bytes).toString();
	  }

}
