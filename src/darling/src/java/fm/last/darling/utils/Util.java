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
package fm.last.darling.utils;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.List;
import java.util.Map;

import org.ho.yaml.Yaml;

import fm.last.darling.nspace.Dimension;

public class Util {

  public static String epochtoYMD(long epoch) {
    Calendar thence = new GregorianCalendar();
    thence.setTimeInMillis(epoch * 1000);
    int year = thence.get(Calendar.YEAR);
    int month = thence.get(Calendar.MONTH) + 1;
    int day = thence.get(Calendar.DAY_OF_MONTH);
    return String.format("%04d%02d%02d", year, month, day);
  }

  public static List<List<Dimension>> readRequestedProjections(File yamlFile) throws FileNotFoundException {

    List<List<Dimension>> result = new ArrayList<List<Dimension>>();
    
    // open file, read yaml, turn into pumpkin.
    Map<String, ?> yaml = (Map) Yaml.load(yamlFile);

    List<String> projections = (List<String>) yaml.get("projections");
    if(projections == null || projections.isEmpty()) {
      return result;
    }
    
    for (String projectionName : projections) {
      String[] dimensionNames = projectionName.split("-");
      List<Dimension> dimensions = new ArrayList<Dimension>();
      
      for (String dimension : dimensionNames) {
        dimensions.add(new Dimension(dimension));
      }
      
      result.add(dimensions);
    }
    
    return result;
  }
}
