import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class LocalCache {
  static const _historyKey = 'cached_history';
  static const _tipsKey = 'cached_tips';

  Future<void> saveHistory(List<dynamic> items) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_historyKey, jsonEncode(items));
  }

  Future<List<dynamic>> loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_historyKey);
    if (raw == null) return [];
    return jsonDecode(raw) as List<dynamic>;
  }

  Future<void> saveTips(List<dynamic> items) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tipsKey, jsonEncode(items));
  }

  Future<List<dynamic>> loadTips() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_tipsKey);
    if (raw == null) return [];
    return jsonDecode(raw) as List<dynamic>;
  }
}
