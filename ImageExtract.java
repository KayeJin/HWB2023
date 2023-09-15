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


//并行执行
import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ImageExtract {
    public static void main(String[] args) {
        // 设置Tessdata环境变量
        System.setProperty("TESSDATA_PREFIX", "/usr/share/tesseract-ocr2/5/tessdata/directory");

        // 输入图片文件夹路径和输出txt文件路径
        String inputFolderPath = "/home/liu-shutong/Share/001/ppt_png";
        String outputTxtFilePath = "/home/liu-shutong/Share/002/output.txt";

        File inputFolder = new File(inputFolderPath);
        File[] imageFiles = inputFolder.listFiles((dir, name) ->
                name.toLowerCase().endsWith(".jpg") || name.toLowerCase().endsWith(".png"));

        ITesseract tess = new Tesseract();
        tess.setLanguage("chi_sim+eng"); // 设置识别语言为英文（可以根据需要更改）

        int numThreads = Runtime.getRuntime().availableProcessors(); // 获取可用的处理器核心数
        ExecutorService executorService = Executors.newFixedThreadPool(numThreads);

        List<File> processedFiles = new ArrayList<>();

        try (FileWriter writer = new FileWriter(outputTxtFilePath)) {
            for (File imageFile : imageFiles) {
                executorService.submit(() -> {
                    try {
                        String extractedText = tess.doOCR(imageFile);
                        synchronized (writer) {
                            writer.write("Extracted Text from " + imageFile.getName() + ":\n");
                            writer.write(extractedText + "\n\n");
                        }
                        processedFiles.add(imageFile);
                    } catch (IOException | TesseractException e) {
                        e.printStackTrace();
                    }
                });
            }

            // 关闭并等待所有任务完成
            executorService.shutdown();
            executorService.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);

            // 打印已处理的文件列表
            System.out.println("Processed Files:");
            for (File processedFile : processedFiles) {
                System.out.println(processedFile.getName());
            }

            System.out.println("Text extraction completed. Output written to " + outputTxtFilePath);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
