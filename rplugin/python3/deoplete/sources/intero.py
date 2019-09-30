from .base import Base
import re

CompleteResults = "g:intero_complete_result"

class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.rank = 1000
        self.name = "intero"
        self.mark = "[intero]"
        self.sorters = ["sorter_rank"]
        self.filetypes = ["haskell"]

    def get_complete_position(self, context):
        m = re.search(r"([A-Z]\w*\.)*\w*$", context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        if context["is_async"]:
            result = self.vim.eval(CompleteResults)
            if result != -1:
                context["is_async"] = False
                return [ {"word":word} for word in result ]
        else:
            context["is_async"] = True
            self.vim.command("let {0} = -1".format(CompleteResults))
            self.vim.call('intero#repl#complete')
        return []

