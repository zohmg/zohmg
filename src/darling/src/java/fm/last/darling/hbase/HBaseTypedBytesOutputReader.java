/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package fm.last.darling.hbase;

import java.io.DataInput;
import java.io.IOException;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.streaming.PipeMapRed;
import org.apache.hadoop.streaming.io.OutputReader;
import org.apache.hadoop.typedbytes.Type;
import org.apache.hadoop.typedbytes.TypedBytesInput;
import org.apache.hadoop.typedbytes.TypedBytesWritable;

/**
 * OutputReader that reads the client's output as typed bytes,
 * changes to format suitable for hbase
 */
public class HBaseTypedBytesOutputReader extends OutputReader<ImmutableBytesWritable, Put> {

  private boolean hasGotLastOutput = false;
  private byte[] bytes;
  private DataInput clientIn;
  private ImmutableBytesWritable outKey;
  private Put outValue;
  private TypedBytesInput in;
  
  @Override
  public void initialize(PipeMapRed pipeMapRed) throws IOException {
    super.initialize(pipeMapRed);
    clientIn = pipeMapRed.getClientInput(); // stdout of streaming script.
    in = new TypedBytesInput(clientIn);
  }
  
  @Override
  public boolean readKeyValue() throws IOException {
	  System.err.println("READKEYVALUE ALREADY.\n");
	  
	TypedBytesWritable key = new TypedBytesWritable(); // ineff. prolly
    bytes = in.readRaw();
    if (bytes == null) return false;
    key.set(bytes, 0, bytes.length);
    System.err.println("read once: \n" + bytes.toString());
    
    byte[] rowkey = key.getValue().toString().getBytes("UTF-8");
    outKey = new ImmutableBytesWritable();
    outKey.set(rowkey);

    outValue = new Put(rowkey);

    TypedBytesWritable value = new TypedBytesWritable(); // ineff. prolly
    bytes = in.readRaw();
    if (bytes == null) return false;
    value.set(bytes, 0, bytes.length);
    if(!Type.MAP.equals(value.getType())) {
      throw new IOException("Unexpected type: " + value);
    }
    System.err.println("read twice.\n");

    Set<Map.Entry<String, Integer>> entries = (Set<Entry<String, Integer>>) ((Map) value.getValue()).entrySet();
    for (Map.Entry<String, Integer> entry : entries) {
        String cfq = entry.getKey();
        String[] parts = cfq.split(":");
        if (parts.length < 2)
           continue;
        String family    = parts[0];
        String qualifier = parts[1];

        byte[] val = entry.getValue().toString().getBytes("UTF-8");
        outValue.add(family.getBytes("UTF-8"), qualifier.getBytes("UTF-8"), val);
    }
    hasGotLastOutput = true;
    return true;
  }
  
  @Override
  public ImmutableBytesWritable getCurrentKey() throws IOException {
	  return outKey;
  }

  @Override
  public Put getCurrentValue() throws IOException {
	  return outValue;
  }

  @Override
  public String getLastOutput() {
	  if (hasGotLastOutput)
		  return new ImmutableBytesWritable(bytes).toString();
	  else
		  return "not so much";
  }

}
