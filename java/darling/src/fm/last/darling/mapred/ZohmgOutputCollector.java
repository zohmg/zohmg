package fm.last.darling.mapred;

import java.util.TreeMap;

import org.apache.hadoop.io.IntWritable;

/**
 * encapsulator of data emitted from mapper.
 * 
 * current limitations:
 *   user can specify only a single point in n-space for every invocation.
 *
 */
public class ZohmgOutputCollector {
	private long timestamp;
	private TreeMap<String, String> dimensions;		// point in n-space,
	private TreeMap<String, IntWritable> measurements;	// value(s) at that point.
	
	public ZohmgOutputCollector() {
		dimensions   = new TreeMap<String, String>();
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
