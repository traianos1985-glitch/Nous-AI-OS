package com.nous.companion

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

class CommandReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        val action = intent?.getStringExtra("command") ?: return
        val service = NousAccessibilityService.instance

        Log.i("NOUS_COMPANION", "Received command: $action")

        if (service == null) {
            Log.w("NOUS_COMPANION", "Accessibility service not connected")
            return
        }

        when (action) {
            "back" -> service.pressBack()
            "home" -> service.pressHome()
            "tap" -> {
                val x = intent.getFloatExtra("x", -1f)
                val y = intent.getFloatExtra("y", -1f)
                if (x >= 0 && y >= 0) {
                    service.tap(x, y)
                }
            }
            "ui_tree" -> {
                Log.i("NOUS_COMPANION_UI_TREE", service.rootSummary())
            }
            else -> Log.w("NOUS_COMPANION", "Unknown command: $action")
        }
    }
}
