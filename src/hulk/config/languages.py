from typing import Iterable, Any, List, FrozenSet, Optional, Dict
from hulk.base import Language
from hulk.exceptions import IllegalConfig


class Languages(object):
    """
    Maintains information about the languages that are supported by Hulk.
    """
    @staticmethod
    def from_defs(defs: List[Any],
                  base: 'Optional[Configuration]' = None
                  ) -> 'Languages':
        """
        Loads an operator configuration from a list of definitions taken
        from a configuration file, together with an optionally provided
        parent (overall) configuration.
        """
        config = base.languages if base else Languages()
        for d in defs:
            language = Language.from_dict(d)
            config = config.add(language)
        return config

    def __init__(self,
                 languages: Optional[Dict[str, Languages]] = None
                 ):
        """
        Constructs a collection of lamnguages for a set of languages provided
        in the form a dictionary, indexed by name.
        """
        self.__languages = dict(languages) if languages else {}

    def add(self, language: Language) -> 'Languages':
        """
        Returns a variant of this collection of languages that also includes a
        given language.
        """
        endings = set(self.supported_file_endings)

        # if there already exists a language with the given name, produce a
        # warning and remove its file endings from consideration.
        if language.name in self.__languages:
            old_version = self.__languages[language.name]
            msg = "config overwrites existing language definition: {}.".format(language.name)
            warnings.warn(msg, LanguageOverwriteWarning)
            endings -= set(old_version.file_endings)

        # are the file endings used by this language already in use?
        if language.file_endings & supported_file_endings:
            raise IllegalConfigError("file ending ambiguity: two or more languages share a common file ending.")

        languages = dict(self.__languages)
        languages[language.name] = language
        return Languages(languages)

    def __iter__(self) -> Iterable[Language]:
        """
        An iterator over the languages within this collection.
        """
        for name in self.__languages:
            yield self.__languages[name]

    def __item__(self, name) -> Language:
        """
        Attempts to fetch the definition of the language associated with a
        supplied name.

        Raises:
            KeyError: if no language is found with the given name.
        """
        return self.__languages[name]

    def __contains__(self, name: str) -> bool:
        """
        Provides an alias for `supports`.
        """
        return self.supports(name)

    def supports(self, name: str) -> bool:
        """
        Determines whether this colelctions contains a language with a given
        name.
        """
        return name in self.__languages

    @property
    def supported_file_endings(self) -> FrozenSet[str]:
        """
        The set of file endings that are used by languages within this
        collection.
        """
        endings = set()
        for language in self:
            endings += language.file_endings
        return frozenset(endings)