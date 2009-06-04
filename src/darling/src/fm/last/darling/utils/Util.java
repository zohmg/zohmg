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

  public static ArrayList<ArrayList<Dimension>> readRequestedProjections(File yaml) throws FileNotFoundException {

    // open file, read yaml, turn into pumpkin.
    Object object = Yaml.load(yaml);

    ArrayList<ArrayList<Dimension>> expected = new ArrayList<ArrayList<Dimension>>();
    ArrayList<Dimension> projection0 = new ArrayList<Dimension>();
    projection0.add(new Dimension("country"));
    expected.add(projection0);
    ArrayList<Dimension> projection1 = new ArrayList<Dimension>();
    projection1.add(new Dimension("country"));
    projection1.add(new Dimension("service"));
    expected.add(projection1);

    return expected;
  }
}
