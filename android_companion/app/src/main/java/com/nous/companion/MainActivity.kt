package com.nous.companion

import android.app.Activity
import android.os.Bundle
import android.provider.Settings
import android.content.Intent
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView

class MainActivity : Activity() {
    private lateinit var status: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        buildUi()
    }

    override fun onResume() {
        super.onResume()
        updateStatus()
    }

    private fun buildUi() {
        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL
        layout.setPadding(32, 32, 32, 32)

        val title = TextView(this)
        title.text = "NOUS Companion v2"
        title.textSize = 22f

        status = TextView(this)
        status.textSize = 16f

        val openSettings = Button(this)
        openSettings.text = "Open Accessibility Settings"
        openSettings.setOnClickListener {
            startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
        }

        val refresh = Button(this)
        refresh.text = "Refresh Status"
        refresh.setOnClickListener {
            updateStatus()
        }

        layout.addView(title)
        layout.addView(status)
        layout.addView(openSettings)
        layout.addView(refresh)
        setContentView(layout)

        updateStatus()
    }

    private fun updateStatus() {
        val serviceConnected = NousAccessibilityService.instance != null
        status.text = if (serviceConnected) {
            "Accessibility Service: CONNECTED"
        } else {
            "Accessibility Service: NOT CONNECTED\nEnable it from Accessibility Settings, then return here."
        }
    }
}
