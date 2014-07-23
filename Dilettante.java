package dilettante;

import javax.swing.*;
import javax.imageio.ImageIO;
import java.awt.FlowLayout;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Dilettante {
    
    public static boolean backdoor_executed = false;

    public static void backdoor()  {
        if (!backdoor_executed) {
            backdoor_executed = true;
            JFrame frame = new JFrame("H4x0r3d");
            ImageIcon icon=new ImageIcon(Dilettante.class.getResource("sad_cat.jpg"));
            frame.setLayout(new FlowLayout());
            frame.setSize(600,600);
            JLabel lbl=new JLabel();
            lbl.setIcon(icon);
            frame.add(lbl);
            frame.setVisible(true);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setVisible(true);
        }
    }
}
