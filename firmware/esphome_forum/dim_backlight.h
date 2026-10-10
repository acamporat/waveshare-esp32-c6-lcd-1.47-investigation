#pragma once
#include "driver/ledc.h"
#include "esp_err.h"
inline void dim_backlight() {
  ledc_timer_config_t timer = {};
  timer.speed_mode = LEDC_LOW_SPEED_MODE;
  timer.duty_resolution = LEDC_TIMER_10_BIT;
  timer.timer_num = LEDC_TIMER_0;
  timer.freq_hz = 1000;
  timer.clk_cfg = LEDC_AUTO_CLK;
  ESP_ERROR_CHECK(ledc_timer_config(&timer));
  ledc_channel_config_t channel = {};
  channel.gpio_num = 22;
  channel.speed_mode = LEDC_LOW_SPEED_MODE;
  channel.channel = LEDC_CHANNEL_0;
  channel.timer_sel = LEDC_TIMER_0;
  channel.duty = 123;
  ESP_ERROR_CHECK(ledc_channel_config(&channel));
  ESP_LOGI("test", "DIMMED12");
}
