import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium.webdriver.chrome.webdriver import WebDriver

from donation.models import PartnerCharity


@override_settings(CREDIT_CARD_RATE_LIMIT_ENABLED=False)
class DonationFormTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(DonationFormTestCase, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

    def setUp(self):
        PartnerCharity.objects.update_or_create(slug_id='test_charity', defaults={'name': 'Test Charity'})
        PartnerCharity.objects.update_or_create(slug_id='test_charity2', defaults={'name': 'Test Charity 2'})
        PartnerCharity.objects.update_or_create(slug_id='eaa', defaults={'name': 'Effective Altruism Australia'})
        PartnerCharity.objects.update_or_create(slug_id='unallocated', defaults={'name': 'our partner charities'})

    def initialise_form(self, charity=None):
        url_params = '?charity=%s' % charity if charity else ''
        self.selenium.get('%s%s%s' % (self.live_server_url, '/pledge_new/', url_params))

    def select_allocate_donation(self, allocate=False):
        option_number = 2 if allocate else 1
        self.selenium.find_element_by_id('id-donate-option-%s' % option_number).click()

    def select_frequency(self, one_time=True):
        buttons = self.selenium.find_element_by_class_name('frequency-options').find_elements_by_css_selector('label')
        buttons[0 if one_time else 1].click()

    def select_donation_amount(self, amount=25):
        if amount in (25, 50, 100, 250):
            self.selenium.find_element_by_id('id-amount-%s' % amount).click()
        else:
            self.selenium.find_element_by_id('id-amount-other').click()
            input = self.selenium.find_element_by_name('amount.value')
            input.send_keys(amount)

    def populate_contribute_to_eaa(self, amount=25):
        self.selenium.find_element_by_id('id_will_contribute').click()
        input = self.selenium.find_element_by_name('contribute.value')
        input.send_keys(amount)

    def select_donation_amount_allocate(self, amounts=[100]):
        div = self.selenium.find_element_by_id('id-allocate-donation-section')
        inputs = div.find_elements_by_css_selector('input')
        for i in range(min(len(inputs), len(amounts))):
            input = inputs[i]
            input.send_keys(amounts[i])

    def populate_donor_details(self, **kwargs):
        form_values = {
            'name': 'Donor name',
            'email': 'email@example.com',
            'subscribe': True,
        }
        form_values.update(kwargs)
        name_input = self.selenium.find_element_by_name('name')
        name_input.send_keys(form_values['name'])

        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys(form_values['email'])

        if form_values['subscribe']:
            self.selenium.find_element_by_id('id_subscribe').click()

    def select_payment_type(self, bank_transfer=True):
        id_used = 'id-bank-transfer' if bank_transfer else 'id-credit-card'
        self.selenium.find_element_by_xpath("//label[@for='%s']" % id_used).click()

    def populate_credit_card(self, **kwargs):
        form_values = {
            'cardName': 'Donor name',
            'cardNumber': '4200000000000000',  # Valid VISA test card
            'cardExpiry': '1023',
            'cardCVC': '123',
            'cardAddress': '25 Bourke st',
            'cardCity': 'Melbourne',
            'cardState': 'Victoria',
            'cardPostcode': '3000',
            'cardCountry': 'Australia',
        }
        form_values.update(kwargs)

        for field_name, value in form_values.items():
            input = self.selenium.find_element_by_name('payment.%s' % field_name)
            input.send_keys(value)

    def populate_gift(self, **kwargs):
        self.selenium.find_element_by_id('id_donation_is_gift').click()
        form_values = {
            'recipient_name': 'Recipient Name',
            'recipient_email': 'recipient@example.com',
            'personal_message': 'Gift message'
        }
        form_values.update(kwargs)
        for field_name, value in form_values.items():
            input = self.selenium.find_element_by_name('gift.%s' % field_name)
            input.send_keys(value)

    def submit_form(self, wait_seconds=3):
        self.selenium.find_element_by_class_name('btn-success').click()
        self.selenium.implicitly_wait(wait_seconds)

    def get_calculated_total(self):
        outer_div = self.selenium.find_element_by_class_name('total-amount-group')
        element = outer_div.find_element_by_css_selector('input')
        return float(element.get_attribute('value'))

    def assert_is_on_final_screen(self):
        self.assertGreater(len(self.selenium.find_elements_by_class_name('complete-other-info')), 0)

    def assert_is_not_final_screen(self):
        self.assertEqual(len(self.selenium.find_elements_by_class_name('complete-other-info')), 0)

    def assert_warnings(self, num_warnings=1):
        self.assertEqual(len(self.selenium.find_elements_by_class_name('text-danger')), num_warnings)

    def complete_form(self, allocate=False, one_time=True, amounts=[100], donor_details=None,
                      bank_transfer=False, card_details=None, assert_total_calculation=None,
                      contribute=None, is_gift=False, gift_details=None, charity=None):
        self.initialise_form(charity)
        if charity is None:
            self.select_allocate_donation(allocate=allocate)
        self.select_frequency(one_time=one_time)
        if allocate:
            self.select_donation_amount_allocate(amounts=amounts)
        else:
            self.select_donation_amount(amount=amounts[0])

        if contribute:
            self.populate_contribute_to_eaa(amount=contribute)

        if assert_total_calculation:
            assert self.get_calculated_total() == assert_total_calculation

        self.populate_donor_details(**(donor_details or {}))
        self.select_payment_type(bank_transfer=bank_transfer)
        if not bank_transfer:
            self.populate_credit_card(**(card_details or {}))

        if is_gift:
            self.populate_gift(**(gift_details or {}))

        if bank_transfer:
            self.submit_form()
        else:
            self.submit_form(wait_seconds=10)

    def test_credit_card(self):
        self.complete_form(bank_transfer=False)
        self.assert_is_on_final_screen()

    def test_bank_transfer(self):
        self.complete_form(bank_transfer=True)
        self.assert_is_on_final_screen()

    def test_contribute_to_eaa(self):
        self.complete_form(bank_transfer=True, contribute=50, amounts=[100], assert_total_calculation=150)
        self.assert_is_on_final_screen()

    def test_custom_donation_amount(self):
        self.complete_form(bank_transfer=True, amounts=[12345])
        self.assert_is_on_final_screen()

    def test_recurring_bank_transfer(self):
        self.complete_form(one_time=False, bank_transfer=True)
        self.assert_is_on_final_screen()

    def test_incomplete_donor_details(self):
        self.complete_form(one_time=False, bank_transfer=True, donor_details={'name': ''})
        self.assert_warnings(1)

    def test_incomplete_credit_card_info(self):
        self.complete_form(one_time=True, bank_transfer=False, card_details={'cardName': ''})
        self.assert_warnings(1)

    def test_declined_credit_card(self):
        self.complete_form(bank_transfer=False, card_details={'cardNumber': '5560000000000001'})
        self.assert_warnings(1)

    def test_invalid_credit_card_expiry(self):
        self.complete_form(one_time=True, bank_transfer=False, card_details={'cardExpiry': '1017'})
        self.assert_warnings(1)

    def test_invalid_credit_card_cvc(self):
        self.complete_form(one_time=True, bank_transfer=False, card_details={'cardCVC': '12'})
        self.assert_warnings(1)

    def test_manually_allocated_donation(self):
        self.complete_form(bank_transfer=True, allocate=True, amounts=[100, 200], assert_total_calculation=300)
        self.selenium.implicitly_wait(10)
        self.assert_is_on_final_screen()

    def test_gift(self):
        self.complete_form(is_gift=True, bank_transfer=False)
        self.assert_is_on_final_screen()

    def test_gift_details_incomplete(self):
        self.complete_form(is_gift=True, bank_transfer=True, gift_details={'recipient_email': 'hi@'})
        self.assert_is_not_final_screen()

    def test_recurring_credit_card_impossible(self):
        self.initialise_form()
        self.select_frequency(one_time=False)
        cc_button = self.selenium.find_element_by_xpath("//label[@for='%s']" % 'id-credit-card')
        self.assertEqual(cc_button.get_attribute('disabled'), 'true')

    @override_settings(CREDIT_CARD_RATE_LIMIT_ENABLED=True)
    def test_credit_card_rate_limit(self):
        for i in range(7):
            self.complete_form(bank_transfer=False)
            time.sleep(5)
        self.assert_warnings(1)

    def test_direct_donation(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/pledge_new/?charity=test_charity'))
        self.assertTrue(
            'Test Charity' in self.selenium.find_element_by_css_selector('form').find_element_by_css_selector(
                'h2').text)
        self.complete_form(bank_transfer=True, charity='test_charity')
        self.assert_is_on_final_screen()
