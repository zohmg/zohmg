package fm.last.darling.user;

import fm.last.darling.mapred.ZohmgOutputCollector;

// this is what the user's mapper will look like.
public class ExampleMapper implements UserMapper {
	public void map(String key, String value, ZohmgOutputCollector collector) {
		String parts[] = value.split("\t");
		if (parts.length < 4) {
			System.err.println("split failed." + parts.length);
			return;
		}

		collector.setTimestamp(new Long(parts[0]));
		collector.addDimension("country", parts[1]);
		collector.addDimension("service", parts[2]);
		collector.addValue("hits", 1);
		collector.addValue("bytes", new Integer(parts[3]));
		
		System.out.println("example-mapper done.");
	}
}
