package fm.last.darling.user;

import fm.last.darling.mapred.ZohmgOutputCollector;

// this is what the user's mapper will look like.
public class ExampleMapper {
	public void map(String key, String value, ZohmgOutputCollector collector) {
		String parts[] = value.split("\t");
		if (parts.length < 3)
			return;
		
		collector.setTimestamp(new Integer(parts[0]));
		collector.addDimension("country", parts[1]);
		collector.addDimension("service", parts[2]);
		collector.addValue("users", 1);		
	}
}
