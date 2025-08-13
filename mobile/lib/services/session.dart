import 'package:flutter/foundation.dart';

class SessionState extends ChangeNotifier {
  String? token;
  String locale = 'en';

  void setToken(String value) {
    token = value;
    notifyListeners();
  }

  void clear() {
    token = null;
    notifyListeners();
  }

  void setLocale(String value) {
    locale = value;
    notifyListeners();
  }
}
