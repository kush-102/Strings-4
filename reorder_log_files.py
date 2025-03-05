class Solution:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        def log_key(log):
            identifier, rest = log.split(" ", 1)
            if rest[0].isdigit():
                return (1,)
            else:
                return (0, rest, identifier)

        return sorted(logs, key=log_key)

    # time complexity is O(k*nlogn)  where k is the length of the log and n is the number of logs
    # space complexity is O(n*k)
