import json
import re
import os

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen    

# Decoders for API Output - TODO: Proper error handling
def _decode_json (s):
    if s == '':
        return None
    return json.loads(s)

def _decode_lines (s, linefunc):
    if s == '':
        return []
    
    lines = s.strip().split('\n')
    result = []
    for line in lines:
        result.append(linefunc(line))
            
    return result

def _decode_cercaNumeroTrenoTrenoAutocomplete (s):
    def linefunc (line):
        r = re.search('^(\d+)\s-\s(.+)\|(\d+)-(.+)$', line)
        if r is not None:
            return r.group(2,4)
        
    return _decode_lines (s, linefunc)

def _decode_autocompletaStazione (s):
    return _decode_lines (s, lambda line: tuple(line.strip().split('|')))


class API:
    def __init__ (self, **options):
        self.__verbose = options.get('verbose', False)
        self.__urlopen = options.get('urlopen', urlopen)
        self.__plainoutput = options.get('plainoutput', False)
        self.__decoders = {
            'andamentoTreno':     _decode_json,
            'cercaStazione':      _decode_json,
            'tratteCanvas':       _decode_json,
            'dettaglioStazione':  _decode_json,
            'regione':            _decode_json,
            'cercaNumeroTrenoTrenoAutocomplete': _decode_cercaNumeroTrenoTrenoAutocomplete,
            'autocompletaStazione': _decode_autocompletaStazione
        }
        self.__default_decoder = lambda x: x

    def __checkAndDecode(self, function, data):
        decoder = self.__decoders.get(function, self.__default_decoder)
        return decoder(data)
        
    def call (self, function, *params, **options):
        plain = options.get('plainoutput', self.__plainoutput)
        verbose = options.get('verbose', self.__verbose)
        
        base = 'http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/'
        path = '/'.join(str(p) for p in params)
        url = base + function + '/' + path

        if verbose:
            print (url)

        req = self.__urlopen(url)
        data = req.read().decode('utf-8')
        if plain:
            return data
        else:
            return self.__checkAndDecode (function, data)


