plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.pranshul.sigdeck"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.pranshul.sigdeck"
        minSdk = 26
        targetSdk = 34
        versionCode = 10
        versionName = "2.1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"