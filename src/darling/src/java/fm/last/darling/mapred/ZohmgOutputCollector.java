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
package fm.last.darling.mapred;

import java.util.TreeMap;

import org.apache.hadoop.io.IntWritable;

/**
 * encapsulator of data emitted from mapper. current limitations: user can specify only a single point in n-space for
 * every invocation.
 */
public class ZohmgOutputCollector {
  private long timestamp;
  private TreeMap<String, String> dimensions; // point in n-space,
  private TreeMap<String, IntWritable> measurements; // value(s) at that point.

  public ZohmgOutputCollector() {
    dimensions = new TreeMap<String, String>();
    measurements = new TreeMap<String, IntWritable>();
  }

  public void setTimestamp(long epoch) {
    timestamp = epoch;
  }

  public long getTimestamp() {
    return timestamp;
  }

  // the name might be misleading: we're not adding a dimension
  // but rather a point along the dimension.
  public void addDimension(String dimension, String value) {
    dimensions.put(dimension, value);
  }

  public TreeMap<String, String> getDimensions() {
    return dimensions;
  }

  public void addMeasurement(String unit, Integer value) {
    measurements.put(unit, new IntWritable(value));
  }

  public TreeMap<String, IntWritable> getMeasurements() {
    return measurements;
  }

  public IntWritable getMeasurement(String unit) {
    return measurements.get(unit);
  }

  public Iterable<String> measurementUnits() {
    return measurements.keySet();
  }

  // TODO.
  public boolean valid() {
    return true;
  }
}
