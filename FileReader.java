import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class fileReader {
	public static void main(String[] args) {
		// 指定输入文件夹的路径
		String inputFolderPath = "/path/";

		// 指定输出txt文件的路径
		String outputTxtFilePath = "/path/";

		try (FileWriter writer = new FileWriter(outputTxtFilePath, true)) {
			// 递归遍历文件夹中的所有文件和子文件夹
			traverseDirectory(new File(inputFolderPath), writer);

			System.out.println("File contents have been written to " + outputTxtFilePath);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void traverseDirectory(File directory, FileWriter writer) throws IOException {
		File[] files = directory.listFiles();
		if (files != null) {
			for (File file : files) {
				if (file.isFile()) {
					// 处理文件
					String fileName = file.getName();
					String fileType = getFileType(fileName);

					// 写入文件名和文件类型信息
					writer.write("File: " + fileName + "\n");
					writer.write("Type: " + fileType + "\n");

					// 读取文件内容并写入到输出文件
					readFileContent(file, writer);
				} else if (file.isDirectory()) {
					// 处理子文件夹
					traverseDirectory(file, writer);
				} else if (file.getName().toLowerCase().endsWith(".zip")) {
					// 处理压缩包
					extractFilesFromZip(file, writer);
				}
			}
		}
	}

	private static String getFileType(String fileName) {
		int dotIndex = fileName.lastIndexOf(".");
		if (dotIndex > 0) {
			return fileName.substring(dotIndex + 1);
		}
		return "Unknown";
	}

	private static void readFileContent(File file, FileWriter writer) throws IOException {
		try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
			writer.write("Content:\n");
			String line;
			while ((line = reader.readLine()) != null) {
				writer.write(line + "\n");
			}
			writer.write("\n");
		}
	}

	private static void extractFilesFromZip(File zipFile, FileWriter writer) throws IOException {
		try (ZipInputStream zipInputStream = new ZipInputStream(new FileInputStream(zipFile))) {
			ZipEntry entry;
			while ((entry = zipInputStream.getNextEntry()) != null) {
				String fileName = entry.getName();
				String fileType = getFileType(fileName);

				// 写入文件名和文件类型信息
				writer.write("File: " + fileName + "\n");
				writer.write("Type: " + fileType + " (from ZIP)\n");

				// 读取文件内容并写入到输出文件
				readFileContentFromZip(zipInputStream, writer);
			}
		}
	}

	private static void readFileContentFromZip(ZipInputStream zipInputStream, FileWriter writer) throws IOException {
		writer.write("Content:\n");
		BufferedReader reader = new BufferedReader(new InputStreamReader(zipInputStream));
		String line;
		while ((line = reader.readLine()) != null) {
			writer.write(line + "\n");
		}
		writer.write("\n");
	}
}
