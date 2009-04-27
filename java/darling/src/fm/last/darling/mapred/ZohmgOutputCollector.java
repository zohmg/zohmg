package fm.last.darling.mapred;

import java.util.HashMap;
import java.util.Map;

// encapsulator of data emitted from mapper.
public class ZohmgOutputCollector {
	private long timestamp;
	private Map<String, String> dimensions; // point in n-space,
	private Map<String, Integer> values;    // value(s) at that point.
	
	public ZohmgOutputCollector() {
		dimensions = new HashMap<String, String>();
		values     = new HashMap<String, Integer>();
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
	public Map<String, String> getDimensions() {
		return dimensions;
	}
	
	public void addValue(String unit, Integer value) {
		values.put(unit, value);
	}
	public Map<String, Integer> getValues() {
		return values;
	}
	
	// TODO.
	public boolean valid() {
		return true;
	}
}
