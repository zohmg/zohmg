package fm.last.darling.mapred;

import java.util.HashMap;
import java.util.Map;

// encapsulator of data emitted from mapper.
public class ZohmgOutputCollector {
	private int timestamp;
	private Map<String, String> dimensions; // point in n-space,
	private Map<String, Integer> values;    // value(s) at that point.
	
	public ZohmgOutputCollector() {
		dimensions = new HashMap<String, String>();
		values     = new HashMap<String, Integer>();
	}
	
	public void setTimestamp(int epoch) {
		timestamp = epoch;
	}
	public int getTimestamp() {
		return timestamp;
	}
	
	// the name might be misleading: we're not adding a dimension
	// but rather a point along the dimension.
	public void addDimension(String dimension, String value) {
		dimensions.put(dimension, value);
	}
	
	public void addValue(String unit, Integer value) {
		values.put(unit, value);
	}
}
