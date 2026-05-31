package com.nous.companion

import android.app.Activity
import android.os.Bundle
import android.provider.Settings
import android.content.Intent
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView

class MainActivity : Activity() {

    private lateinit var statusView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL
        layout.setPadding(32, 32, 32, 32)

        val title = TextView(this)
        title.text = "NOUS Companion v2"
        title.textSize = 22f

        statusView = TextView(this)
        statusView.textSize = 16f

        val settingsButton = Button(this)
        settingsButton.text = "Open Accessibility Settings"
        settingsButton.setOnClickListener {
            startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
        }

        val refreshButton = Button(this)
        refreshButton.text = "Refresh Status"
        refreshButton.setOnClickListener {
            updateStatus()
        }

        layout.addView(title)
        layout.addView(statusView)
        layout.addView(settingsButton)
        layout.addView(refreshButton)

        setContentView(layout)

        updateStatus()
    }

    override fun onResume() {
        super.onResume()
        updateStatus()
    }

    private fun updateStatus() {
        val connected = NousAccessibilityService.instance != null

        statusView.text =
            if (connected)
                "Accessibility Service: CONNECTED"
            else
                "Accessibility Service: NOT CONNECTED"
    }
}
