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
package fm.last.darling.user;

import fm.last.darling.mapred.ZohmgOutputCollector;

// this is what the user's mapper will look like.
public class ExampleMapper implements UserMapper {
  public void map(long key, String value, ZohmgOutputCollector collector) {
    String parts[] = value.split("\t");
    if (parts.length < 4) {
      System.err.println("split failed." + parts.length);
      return;
    }

    Long ts;
    Integer bytes;
    try {
      ts = new Long(parts[0]);
      bytes = new Integer(parts[3]);
    } catch (Exception e) {
      System.err.println("malformated data on key " + key);
      return;
    }

    collector.setTimestamp(ts); // unix time, obv.
    collector.addDimension("country", parts[1]);
    collector.addDimension("service", parts[2]);
    collector.addDimension("generator", "SR400");
    collector.addMeasurement("hits", 1);
    collector.addMeasurement("bytes", bytes);
  }
}
