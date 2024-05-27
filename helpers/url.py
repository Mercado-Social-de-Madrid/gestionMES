
def remove_special_chars(url):
    reserved_chars = "!*'();:@&=+$,/?#[]"
    cleaned_url = ''.join(char for char in url if char not in reserved_chars)
    return cleaned_url