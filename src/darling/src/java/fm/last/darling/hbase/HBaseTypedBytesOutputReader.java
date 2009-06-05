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

import org.apache.hadoop.hbase.io.BatchUpdate;
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
public class HBaseTypedBytesOutputReader extends OutputReader<ImmutableBytesWritable, BatchUpdate> {

  private byte[] bytes;
  private DataInput clientIn;
  private ImmutableBytesWritable outKey;
  private BatchUpdate outValue;
  private TypedBytesWritable tmpValue;
  private TypedBytesInput in;
  
  @Override
  public void initialize(PipeMapRed pipeMapRed) throws IOException {
    super.initialize(pipeMapRed);
    clientIn = pipeMapRed.getClientInput();
    outKey = new ImmutableBytesWritable();
    outValue = new BatchUpdate();
    tmpValue = new TypedBytesWritable();
    in = new TypedBytesInput(clientIn);
  }
  
  @Override
  public boolean readKeyValue() throws IOException {
    bytes = in.readRaw();
    if (bytes == null) {
      return false;
    }
    tmpValue.set(bytes, 0, bytes.length);
    outKey.set(tmpValue.getValue().toString().getBytes("UTF-8"));
    
    bytes = in.readRaw();
    tmpValue.set(bytes, 0, bytes.length);
    if(!Type.MAP.equals(tmpValue.getType())) {
      throw new IOException("Unexpected type: " + tmpValue);
    }
    Set<Map.Entry<String, Integer>> entries = (Set<Entry<String, Integer>>) ((Map) tmpValue.getValue()).entrySet();
    for (Map.Entry<String, Integer> entry : entries) {
      outValue.put(entry.getKey(), entry.getValue().toString().getBytes("UTF-8"));
    }
    return true;
  }
  
  @Override
  public ImmutableBytesWritable getCurrentKey() throws IOException {
    return outKey;
  }
  
  @Override
  public BatchUpdate getCurrentValue() throws IOException {
    return outValue;
  }

  @Override
  public String getLastOutput() {
    return new TypedBytesWritable(bytes).toString();
  }

}
