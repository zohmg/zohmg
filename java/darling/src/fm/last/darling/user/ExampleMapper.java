package fm.last.darling.user;

import fm.last.darling.mapred.ZohmgOutputCollector;

// this is what the user's mapper will look like.
public class ExampleMapper implements UserMapper {
	public void map(long key, String value, ZohmgOutputCollector collector) {
		String parts[] = value.split("\t");
		if (parts.length < 4) {
			System.err.println("split failed." + parts.length);
			return;
		}

		Long ts;
		Integer bytes;
		try {
			ts = new Long(parts[0]);
			bytes = new Integer(parts[3]);
		} catch (Exception e) {
			System.err.println("malformated data on key " + key);
			return;
		}

		collector.setTimestamp(ts); // unix time, obv.
		collector.addDimension("country", parts[1]);
		collector.addDimension("service", parts[2]);
		collector.addDimension("generator", "SR400");
		collector.addMeasurement("hits", 1);
		collector.addMeasurement("bytes", bytes);
	}
}
