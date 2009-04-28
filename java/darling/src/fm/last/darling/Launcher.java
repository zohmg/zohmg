package fm.last.darling;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class Launcher {
	public static final Log log = LogFactory.getLog(Launcher.class);

	public static void main(String[] args) throws Exception {
		if (args.length < 1) {
			log.info("ZOHMG!");
			log.info("usage:");
			log.info(" zohmg <input>");
			System.exit(-1);
		}

		String input = args[0].trim();

		ZohmgProgram program = new ZohmgProgram();
		program.start(input);
	}
}
