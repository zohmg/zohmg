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

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.TreeMap;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import fm.last.darling.io.records.NSpacePoint;
import fm.last.darling.nspace.Dimension;
import fm.last.darling.nspace.Projectionist;
import fm.last.darling.user.UserMapper;
import fm.last.darling.utils.Util;

// the class we wrap around the user's mapper.
// TODO FIXME this class is currently not operational
public class MapperWrapper implements Mapper<LongWritable, Text, NSpacePoint, IntWritable> {
  private UserMapper usermapper;
  private ArrayList<ArrayList<Dimension>> rps; 

  public MapperWrapper() throws Exception {
    // TODO: read name of user's mapper class from config.
    String userclass = "fm.last.darling.user.ExampleMapper";

    // dynamically instantiate user's mapper class.
    try {
      usermapper = (UserMapper) Class.forName(userclass).newInstance();
    } catch (Exception e) {
      System.err.println("could not instantiate userclass " + userclass + ": " + e.toString());
      throw new IOException("instantiation fail.");
    }
  }

  public void close() throws IOException {
  }

  public void configure(JobConf conf) {
    try {
      //FIXME TODO this config file is never set, fix fix!
      File datasetDef = new File(conf.get("ZOHMG.DATASET.FILE"));
      rps = Util.readRequestedProjections(datasetDef);
    } catch (FileNotFoundException e) {
      throw new RuntimeException(e);
    }
  }

  // wrap this map around the user's mapper.
  public void map(LongWritable key, Text value, OutputCollector<NSpacePoint, IntWritable> collector, Reporter reporter)
    throws IOException {
    // call on user's mapper
    ZohmgOutputCollector o = new ZohmgOutputCollector();
    usermapper.map(key.get(), value.toString(), o);
    long ts = o.getTimestamp();
    TreeMap<String, String> points = o.getDimensions();

    // fan out into projections,
    
    for (ArrayList<Dimension> requested : rps) {
      // reduce down to the dimensions we are interested in.
      TreeMap<String, String> projection = Projectionist.dimensionality_reduction(requested, points);
      // emit once for every unit.
      for (String unit : o.measurementUnits()) {
        NSpacePoint point = new NSpacePoint(ts, projection, unit);
        collector.collect(point, o.getMeasurement(unit));
      }
    }
  }
}
