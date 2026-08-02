import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SessionState extends ChangeNotifier {
  String? token;
  String locale = 'en';
  String apiBase;

  SessionState({String? initialApiBase})
      : apiBase = initialApiBase ??
            const String.fromEnvironment(
              'API_BASE',
              defaultValue: 'http://localhost:8080',
            );

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    apiBase = prefs.getString('apiBase') ?? apiBase;
    locale = prefs.getString('locale') ?? locale;
    token = prefs.getString('token');
    notifyListeners();
  }

  Future<void> setToken(String value) async {
    token = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', value);
    notifyListeners();
  }

  Future<void> clear() async {
    token = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    notifyListeners();
  }

  Future<void> setLocale(String value) async {
    locale = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('locale', value);
    notifyListeners();
  }

  Future<void> setApiBase(String value) async {
    apiBase = value.trim().replaceAll(RegExp(r'/$'), '');
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('apiBase', apiBase);
    notifyListeners();
  }

  bool get isPt => locale.startsWith('pt');
}
