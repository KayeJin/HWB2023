import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class ImageExtract {
	public static void main(String[] args) {

		// 设置Tessdata环境变量
		System.setProperty("TESSDATA_PREFIX", "/path/");

		// 输入图片文件夹路径和输出txt文件路径
		String inputFolderPath = "/path/";
		String outputTxtFilePath = "/path/";

    //存儲文件名到數組
		File inputFolder = new File(inputFolderPath);
		File[] imageFiles = inputFolder
            .listFiles((dir, name) -> name.toLowerCase().endsWith(".jpg") || name.toLowerCase().endsWith(".png"));

		ITesseract tess = new Tesseract();

    //設置tesseract讀取方式
		tess.setLanguage("chi_sim+eng");

		try (FileWriter writer = new FileWriter(outputTxtFilePath)) {
			for (File imageFile : imageFiles) {

				String extractedText = tess.doOCR(imageFile);
				writer.write("Extracted Text from " + imageFile.getName() + ":\n");
				writer.write(extractedText + "\n\n");

			}
			System.out.println("Text extraction completed. Output written to " + outputTxtFilePath);
		} catch (IOException | TesseractException e) {

		}
	}
}
