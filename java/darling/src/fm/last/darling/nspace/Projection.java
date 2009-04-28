package fm.last.darling.nspace;

import java.util.Collection;
import java.util.Iterator;
import java.util.TreeMap;

import fm.last.darling.io.records.NSpacePoint;

// a projection is a subspace of nspace, or whatever.
public class Projection {
	private TreeMap<String, String> dimensions;
	private final String delimiter = "-";

	public Projection() { }
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
		if (c.isEmpty()) return "";
		Iterator<String> iter = c.iterator();
		StringBuffer buffer = new StringBuffer(iter.next());
		while (iter.hasNext())
			buffer.append(delimiter).append(iter.next());
		return buffer.toString();
	}
}
