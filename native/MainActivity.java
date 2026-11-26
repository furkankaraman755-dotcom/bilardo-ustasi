package com.blackballarena.game;

import android.os.Build;
import android.os.Bundle;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import androidx.activity.OnBackPressedCallback;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import android.content.ContentValues;
import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        // 0-03 / 0-02: dosyaya yedek ve metin paylaşma köprüsü (oyunda: Capacitor.Plugins.BbaNative)
        registerPlugin(BbaNativePlugin.class);
        super.onCreate(savedInstanceState);
        tamEkran();
        // Telefonun sistem yazı boyutu, görsellere birebir kurulan ekranları bozmasın
        try { getBridge().getWebView().getSettings().setTextZoom(100); } catch (Exception e) { }
        // Android geri tuşu: oyunun kendi geri mantığına sorulur (pencereyi kapat / önceki sayfa);
        // ana menüdeyse uygulama kapanmaz, arka plana alınır
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                try {
                    getBridge().getWebView().evaluateJavascript(
                        "(window.bbaBack?window.bbaBack():'exit')",
                        v -> { if (v == null || v.contains("exit")) moveTaskToBack(true); });
                } catch (Exception e) {
                    moveTaskToBack(true);
                }
            }
        });
    }

    @Override
    public void onResume() {
        super.onResume();
        tamEkran();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) tamEkran();
    }

    private void tamEkran() {
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        if (Build.VERSION.SDK_INT >= 28) {
            WindowManager.LayoutParams lp = getWindow().getAttributes();
            lp.layoutInDisplayCutoutMode = Build.VERSION.SDK_INT >= 30
                ? WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS
                : WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            getWindow().setAttributes(lp);
        }
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }

    /** Oyun içinden: Capacitor.Plugins.BbaNative.saveText({name, text}) ve shareText({title, text}) */
    @CapacitorPlugin(name = "BbaNative")
    public static class BbaNativePlugin extends Plugin {
        @PluginMethod
        public void saveText(PluginCall call) {
            try {
                String name = call.getString("name", "yedek.txt").replaceAll("[^A-Za-z0-9._-]", "_");
                byte[] data = call.getString("text", "").getBytes(StandardCharsets.UTF_8);
                String yer;
                if (Build.VERSION.SDK_INT >= 29) {
                    ContentValues v = new ContentValues();
                    v.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
                    v.put(MediaStore.MediaColumns.MIME_TYPE, "text/plain");
                    v.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/BlackballArena");
                    Uri uri = getContext().getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, v);
                    if (uri == null) { call.reject("dosya oluşturulamadı"); return; }
                    try (OutputStream o = getContext().getContentResolver().openOutputStream(uri)) { o.write(data); }
                    yer = "İndirilenler/BlackballArena/" + name;
                } else {
                    File dir = new File(getContext().getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), "BlackballArena");
                    if (!dir.exists()) dir.mkdirs();
                    File f = new File(dir, name);
                    try (FileOutputStream o = new FileOutputStream(f)) { o.write(data); }
                    yer = f.getAbsolutePath();
                }
                JSObject r = new JSObject();
                r.put("path", yer);
                call.resolve(r);
            } catch (Exception e) {
                call.reject(String.valueOf(e.getMessage()));
            }
        }

        @PluginMethod
        public void shareText(PluginCall call) {
            try {
                String title = call.getString("title", "Blackball Arena");
                Intent i = new Intent(Intent.ACTION_SEND);
                i.setType("text/plain");
                i.putExtra(Intent.EXTRA_SUBJECT, title);
                i.putExtra(Intent.EXTRA_TEXT, call.getString("text", ""));
                Intent c = Intent.createChooser(i, title);
                c.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                getActivity().runOnUiThread(() -> getContext().startActivity(c));
                call.resolve();
            } catch (Exception e) {
                call.reject(String.valueOf(e.getMessage()));
            }
        }
    }
}
