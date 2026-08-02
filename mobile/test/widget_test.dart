import 'package:flutter_test/flutter_test.dart';
import 'package:cofreseguro/l10n/app_strings.dart';

void main() {
  test('AppStrings EN/PT', () {
    expect(AppStrings('en').signIn, 'Sign in');
    expect(AppStrings('pt').signIn, 'Entrar');
  });
}
