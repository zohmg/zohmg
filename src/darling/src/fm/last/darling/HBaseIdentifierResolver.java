/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package fm.last.darling;

import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.streaming.io.IdentifierResolver;
import org.apache.hadoop.streaming.io.TextInputWriter;

/**
 * By setting <tt>stream.io.identifier.resolver.class=HBaseIdentifierResolver</tt> and giving
 * <tt>-outputformat org.apache.hadoop.hbase.mapred.TableOutputFormat</tt> to dumbo you will be able to store stuff in
 * HBase. Pro-tip: Remember to set <tt>hbase.mapred.outputtable</tt>.
 */
public class HBaseIdentifierResolver extends IdentifierResolver {
  public static final String HBASE_ID = "hbase";

  /**
   * Tries to resolve a given identifier, falls back on super class.
   */
  public void resolve(String identifier) {
    if (identifier.equalsIgnoreCase(HBASE_ID)) {
      System.err.println("HBaseIdentifierResolver.resolve: HBASE.\n");
      setInputWriterClass(TextInputWriter.class);
      setOutputReaderClass(HBaseOutputReader.class);
      setOutputKeyClass(ImmutableBytesWritable.class);
      setOutputValueClass(BatchUpdate.class);
    } else {
      super.resolve(identifier);
    }
  }
}
