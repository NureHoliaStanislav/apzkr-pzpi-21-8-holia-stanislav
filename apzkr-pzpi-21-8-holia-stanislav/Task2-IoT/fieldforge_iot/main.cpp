#include <iostream>
#include <fstream>
#include <cpr/cpr.h>
#include <string>
#include <map>
#include <random>



// Function to read settings from a file
std::map<std::string, std::string> readSettings() {
    std::map<std::string, std::string> settings;
    std::ifstream settings_file("settings.txt");
    if (settings_file.is_open()) {
        std::string line;
        while (std::getline(settings_file, line)) {
            size_t pos = line.find("=");
            if (pos != std::string::npos) {
                std::string key = line.substr(0, pos);
                std::string value = line.substr(pos + 1);
                settings[key] = value;
            }
        }
        settings_file.close();
    }
    return settings;
}

// Function to write settings to a file
void writeSettings(const std::map<std::string, std::string>& settings) {
    std::ofstream settings_file("settings.txt");
    if (settings_file.is_open()) {
        for (const auto& pair : settings) {
            settings_file << pair.first << "=" << pair.second << "\n";
        }
        settings_file.close();
    } else {
        std::cout << "Unable to open file\n";
    }
}

// Simulate data received from motion controller
struct MotionData {
    bool motionDetected;
};

// Simulate data that represents the state of the mine
struct DefusionData {
    bool isDefused;
};

// Function to imitate defusing of mine
void defuseMine(DefusionData data) {
    if (data.isDefused) {
        std::cout << "Mine defused!\n";
        std::map<std::string, std::string> settings = readSettings();
        std::string mine_uuid = settings["UUID"].c_str(); 
        std::string api_url = settings["URL"].c_str();
        cpr::Header headers{{"uuid", mine_uuid}};
        cpr::Payload payload{{"is_defused", "true"}};

        auto response = cpr::Put(cpr::Url{api_url}, headers, payload);

        std::cout << "Status code: " << response.status_code << std::endl;
        std::cout << "Response body: " << response.text << std::endl;

    } else {
        std::cout << "Mine not defused.\n";
    }
}

// Function to imitate activation of mine
void activateMine(MotionData data) {
    if (data.motionDetected) {
        std::cout << "Mine activated!\n";
        std::map<std::string, std::string> settings = readSettings();
        std::string mine_uuid = settings["UUID"].c_str(); 
        std::string api_url = settings["URL"].c_str();
        cpr::Header headers{{"uuid", mine_uuid}};
        cpr::Payload payload{{"is_activated", "true"}};

        auto response = cpr::Put(cpr::Url{api_url}, headers, payload);

        std::cout << "Status code: " << response.status_code << std::endl;
        std::cout << "Response body: " << response.text << std::endl;

    } else {
        std::cout << "No motion detected. Mine not activated.\n";
    }
}
// Simulate receiving data from motion controller
MotionData receiveActivationData() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 9);
    return {dis(gen) == 0};
}

// Simulate receiving data about the state of the mine
DefusionData receiveDefusionData() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 9);
    return {dis(gen) == 0};
}

// Function to reset the mine state
void resetMine() {
    std::cout << "Resetting mine.\n";
    std::map<std::string, std::string> settings = readSettings();
    std::string mine_uuid = settings["UUID"].c_str(); 
    std::string api_url = settings["URL"].c_str();
    cpr::Header headers{{"uuid", mine_uuid}};
    cpr::Payload payload{{"is_activated", "false"}, {"is_defused", "false"}};

    auto response = cpr::Put(cpr::Url{api_url}, headers, payload);

    std::cout << "Status code: " << response.status_code << std::endl;
    std::cout << "Response body: " << response.text << std::endl;
}

int main() {
    std::map<std::string, std::string> settings = readSettings();
    
    if (settings["URL"].empty() || settings["UUID"].empty()) {
        
        std::cout << "Enter URL: ";
        std::getline(std::cin, settings["URL"]);

        std::cout << "Enter UUID: ";
        std::getline(std::cin, settings["UUID"]);
        
        writeSettings(settings);
    }
    
    resetMine();

    while (true) {
        MotionData motionData = receiveActivationData();
        DefusionData defusionData = receiveDefusionData();
        if (motionData.motionDetected) {
            activateMine(motionData);
            return 0;
        }

        if (defusionData.isDefused) {
            defuseMine(defusionData);
            return 0;
        }
        printf("...\n");
        // Sleep for a while to simulate the delay in receiving data
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

}