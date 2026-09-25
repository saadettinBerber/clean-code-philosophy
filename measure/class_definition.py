"""Ölçülen sınıf: alanları, metotları ve sorumluluk kümeleri (Bl.6, Bl.10)."""
import ast
from functools import reduce
from typing import NamedTuple

from measure.findings import Note
from measure.function import Method
from measure.syntax import FUNCTION_NODES


class Cluster(NamedTuple):
    """Birlikte değişen metotlar ve dokundukları alan ya da metot adları."""
    methods: frozenset
    touched: frozenset


class ClassDefinition:
    """Bir sınıfın yapısı; bulguyu kendi yeriyle nota çevirir."""

    def __init__(self, node, scope):
        self._node = node
        self._scope = scope

    def note(self, finding):
        return Note(self._scope.location(self._node), finding)

    def length(self):
        return self._node.end_lineno - self._node.lineno + 1

    def methods(self):
        inside = self._scope.inner(self._node)
        return [Method(node, inside)
                for node in self._node.body if isinstance(node, FUNCTION_NODES)]

    def is_data_structure(self):
        """Metodu olmayan sınıf bir veri yapısıdır; uyum ve melezlik ona uygulanmaz (Bl.6)."""
        return not self.methods()

    def is_test_case(self):
        """Test sınıfı ne nesne ne veri yapısıdır; Bl.6'nın ayrımı ona uygulanmaz."""
        return any(method.is_test() for method in self.methods())

    def constructor_fields(self):
        return {field for method in self.methods() if method.is_constructor() for field in method.assigned_fields()}

    def late_fields(self):
        """Kurucu dışında ilk kez atanan alanlar."""
        return {field for method in self.methods() for field in method.assigned_fields()} - self.constructor_fields()

    def instance_fields(self):
        """Kurucuda atanan alanlar ile dataclass gibi sınıf gövdesinde tür bildirilen alanlar."""
        declared = {node.target.id for node in self._node.body
                    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)}
        return (self.constructor_fields() | declared) - {method.name() for method in self.methods()}

    def field_users(self):
        """Alan → onu kullanan metotlar (kurucular hariç)."""
        others = [method for method in self.methods() if not method.is_constructor()]
        return {field: [m.name() for m in others if field in m.touched_attributes()] for field in self.instance_fields()}

    def responsibility_clusters(self):
        """Alan paylaşan ya da birbirini çağıran metot kümeleri; her küme bir değişme nedeni adayıdır."""
        fields = self.instance_fields()
        clusters = reduce(_merged_with, self._method_clusters(), [])
        return [(sorted(c.methods), sorted(c.touched & fields)) for c in clusters if c.touched & fields]

    def public_state(self):
        """Dışa açık durum: alt çizgisiz alanlar ve public erişimciler (Bl.6 · Hybrids)."""
        fields = sorted(field for field in self.instance_fields() if not field.startswith("_"))
        return fields + sorted(m.name() for m in self.methods() if m.is_public() and m.is_accessor())

    def behavior_methods(self):
        """Erişimci ve adlı kurucu olmayan, anlamlı iş yapan public metotlar (Bl.6 · Hybrids)."""
        return sorted(m.name() for m in self.methods()
                      if m.is_public() and not m.is_special() and not m.is_accessor() and not m.is_named_constructor()
                      and m.does_work())

    def _method_clusters(self):
        """Her metot kendi başına bir küme olarak başlar."""
        names = {method.name() for method in self.methods()}
        reach = self.instance_fields() | names
        return [Cluster(frozenset({m.name()}), frozenset((m.touched_attributes() & reach) | {m.name()}))
                for m in self.methods() if not m.is_constructor()]


def _merged_with(clusters, method):
    """Metodun dokunduğu şeyleri paylaşan kümeler metotla tek kümede birleşir."""
    joined = [cluster for cluster in clusters if cluster.touched & method.touched]
    merged = Cluster(method.methods.union(*(c.methods for c in joined)), method.touched.union(*(c.touched for c in joined)))
    return [cluster for cluster in clusters if cluster not in joined] + [merged]
