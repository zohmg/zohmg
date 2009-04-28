package fm.last.darling.nspace;

import java.util.ArrayList;
import java.util.TreeMap;

// handles projections, obviously.
public class Projectionist {
	public static Projection dimensionality_reduction(ArrayList<Dimension> requested, Projection dimensions) {
		Projection projection = new Projection();
		for (Dimension d : requested)
			projection.put(d, dimensions.get(d));
		return projection;
	}
	public static TreeMap<String,String> dimensionality_reduction(ArrayList<Dimension> requested, TreeMap<String, String> dimensions) {
		TreeMap<String, String> projection = new TreeMap<String, String>();
		for (Dimension d : requested)
			projection.put(d.toString(), dimensions.get(d.toString()));
		return projection;
	}
}
