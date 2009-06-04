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
package fm.last.darling.nspace;

import java.util.Collection;
import java.util.Iterator;
import java.util.TreeMap;

import fm.last.darling.io.records.NSpacePoint;

// a projection is a subspace of nspace, or whatever.
public class Projection {
  private TreeMap<String, String> dimensions;
  private final String delimiter = "-";

  public Projection() {
  }

  public Projection(NSpacePoint point) {
    dimensions = point.getDimensions();
  }

  public void put(Dimension d, String s) {
    dimensions.put(d.toString(), s);
  }

  public String get(Dimension d) {
    return dimensions.get(d.toString());
  }

  public String toHBaseCFQ() {
    return toHBaseColumnFamily() + ":" + toHBaseQualifier();
  }

  public String toHBaseColumnFamily() {
    return join(dimensions.keySet());
  }

  public String toHBaseQualifier() {
    return join(dimensions.values());
  }

  private String join(Collection<String> c) {
    // inspired by http://snippets.dzone.com/posts/show/91
    if (c.isEmpty())
      return "";
    Iterator<String> iter = c.iterator();
    StringBuffer buffer = new StringBuffer(iter.next());
    while (iter.hasNext())
      buffer.append(delimiter).append(iter.next());
    return buffer.toString();
  }
}
