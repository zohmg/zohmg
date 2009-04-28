package fm.last.darling.user;

import fm.last.darling.mapred.ZohmgOutputCollector;

public interface UserMapper {
	public void map(long key, String value, ZohmgOutputCollector collector);
}
