# Generated from MapCSS.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MapCSSParser import MapCSSParser
else:
    from MapCSSParser import MapCSSParser

# This class defines a complete listener for a parse tree produced by MapCSSParser.
class MapCSSListener(ParseTreeListener):

    # Enter a parse tree produced by MapCSSParser#stylesheet.
    def enterStylesheet(self, ctx:MapCSSParser.StylesheetContext):
        pass

    # Exit a parse tree produced by MapCSSParser#stylesheet.
    def exitStylesheet(self, ctx:MapCSSParser.StylesheetContext):
        pass


    # Enter a parse tree produced by MapCSSParser#entry.
    def enterEntry(self, ctx:MapCSSParser.EntryContext):
        pass

    # Exit a parse tree produced by MapCSSParser#entry.
    def exitEntry(self, ctx:MapCSSParser.EntryContext):
        pass


    # Enter a parse tree produced by MapCSSParser#rule_.
    def enterRule_(self, ctx:MapCSSParser.Rule_Context):
        pass

    # Exit a parse tree produced by MapCSSParser#rule_.
    def exitRule_(self, ctx:MapCSSParser.Rule_Context):
        pass


    # Enter a parse tree produced by MapCSSParser#selector.
    def enterSelector(self, ctx:MapCSSParser.SelectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#selector.
    def exitSelector(self, ctx:MapCSSParser.SelectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#simple_selector_operator.
    def enterSimple_selector_operator(self, ctx:MapCSSParser.Simple_selector_operatorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#simple_selector_operator.
    def exitSimple_selector_operator(self, ctx:MapCSSParser.Simple_selector_operatorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#link_selector.
    def enterLink_selector(self, ctx:MapCSSParser.Link_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#link_selector.
    def exitLink_selector(self, ctx:MapCSSParser.Link_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#layer_id_selector.
    def enterLayer_id_selector(self, ctx:MapCSSParser.Layer_id_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#layer_id_selector.
    def exitLayer_id_selector(self, ctx:MapCSSParser.Layer_id_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#simple_selector.
    def enterSimple_selector(self, ctx:MapCSSParser.Simple_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#simple_selector.
    def exitSimple_selector(self, ctx:MapCSSParser.Simple_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#zoom_selector.
    def enterZoom_selector(self, ctx:MapCSSParser.Zoom_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#zoom_selector.
    def exitZoom_selector(self, ctx:MapCSSParser.Zoom_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#quoted.
    def enterQuoted(self, ctx:MapCSSParser.QuotedContext):
        pass

    # Exit a parse tree produced by MapCSSParser#quoted.
    def exitQuoted(self, ctx:MapCSSParser.QuotedContext):
        pass


    # Enter a parse tree produced by MapCSSParser#cssident.
    def enterCssident(self, ctx:MapCSSParser.CssidentContext):
        pass

    # Exit a parse tree produced by MapCSSParser#cssident.
    def exitCssident(self, ctx:MapCSSParser.CssidentContext):
        pass


    # Enter a parse tree produced by MapCSSParser#osmtag.
    def enterOsmtag(self, ctx:MapCSSParser.OsmtagContext):
        pass

    # Exit a parse tree produced by MapCSSParser#osmtag.
    def exitOsmtag(self, ctx:MapCSSParser.OsmtagContext):
        pass


    # Enter a parse tree produced by MapCSSParser#attribute_selector.
    def enterAttribute_selector(self, ctx:MapCSSParser.Attribute_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#attribute_selector.
    def exitAttribute_selector(self, ctx:MapCSSParser.Attribute_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#predicate.
    def enterPredicate(self, ctx:MapCSSParser.PredicateContext):
        pass

    # Exit a parse tree produced by MapCSSParser#predicate.
    def exitPredicate(self, ctx:MapCSSParser.PredicateContext):
        pass


    # Enter a parse tree produced by MapCSSParser#predicate_simple.
    def enterPredicate_simple(self, ctx:MapCSSParser.Predicate_simpleContext):
        pass

    # Exit a parse tree produced by MapCSSParser#predicate_simple.
    def exitPredicate_simple(self, ctx:MapCSSParser.Predicate_simpleContext):
        pass


    # Enter a parse tree produced by MapCSSParser#class_selector.
    def enterClass_selector(self, ctx:MapCSSParser.Class_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#class_selector.
    def exitClass_selector(self, ctx:MapCSSParser.Class_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#pseudo_class_selector.
    def enterPseudo_class_selector(self, ctx:MapCSSParser.Pseudo_class_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#pseudo_class_selector.
    def exitPseudo_class_selector(self, ctx:MapCSSParser.Pseudo_class_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#type_selector.
    def enterType_selector(self, ctx:MapCSSParser.Type_selectorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#type_selector.
    def exitType_selector(self, ctx:MapCSSParser.Type_selectorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#declaration_block.
    def enterDeclaration_block(self, ctx:MapCSSParser.Declaration_blockContext):
        pass

    # Exit a parse tree produced by MapCSSParser#declaration_block.
    def exitDeclaration_block(self, ctx:MapCSSParser.Declaration_blockContext):
        pass


    # Enter a parse tree produced by MapCSSParser#declarations.
    def enterDeclarations(self, ctx:MapCSSParser.DeclarationsContext):
        pass

    # Exit a parse tree produced by MapCSSParser#declarations.
    def exitDeclarations(self, ctx:MapCSSParser.DeclarationsContext):
        pass


    # Enter a parse tree produced by MapCSSParser#declaration.
    def enterDeclaration(self, ctx:MapCSSParser.DeclarationContext):
        pass

    # Exit a parse tree produced by MapCSSParser#declaration.
    def exitDeclaration(self, ctx:MapCSSParser.DeclarationContext):
        pass


    # Enter a parse tree produced by MapCSSParser#declaration_property.
    def enterDeclaration_property(self, ctx:MapCSSParser.Declaration_propertyContext):
        pass

    # Exit a parse tree produced by MapCSSParser#declaration_property.
    def exitDeclaration_property(self, ctx:MapCSSParser.Declaration_propertyContext):
        pass


    # Enter a parse tree produced by MapCSSParser#declaration_value.
    def enterDeclaration_value(self, ctx:MapCSSParser.Declaration_valueContext):
        pass

    # Exit a parse tree produced by MapCSSParser#declaration_value.
    def exitDeclaration_value(self, ctx:MapCSSParser.Declaration_valueContext):
        pass


    # Enter a parse tree produced by MapCSSParser#int_.
    def enterInt_(self, ctx:MapCSSParser.Int_Context):
        pass

    # Exit a parse tree produced by MapCSSParser#int_.
    def exitInt_(self, ctx:MapCSSParser.Int_Context):
        pass


    # Enter a parse tree produced by MapCSSParser#single_value.
    def enterSingle_value(self, ctx:MapCSSParser.Single_valueContext):
        pass

    # Exit a parse tree produced by MapCSSParser#single_value.
    def exitSingle_value(self, ctx:MapCSSParser.Single_valueContext):
        pass


    # Enter a parse tree produced by MapCSSParser#booleanOperator.
    def enterBooleanOperator(self, ctx:MapCSSParser.BooleanOperatorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#booleanOperator.
    def exitBooleanOperator(self, ctx:MapCSSParser.BooleanOperatorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#numericOperator.
    def enterNumericOperator(self, ctx:MapCSSParser.NumericOperatorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#numericOperator.
    def exitNumericOperator(self, ctx:MapCSSParser.NumericOperatorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#valueOperator.
    def enterValueOperator(self, ctx:MapCSSParser.ValueOperatorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#valueOperator.
    def exitValueOperator(self, ctx:MapCSSParser.ValueOperatorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#regexOperator.
    def enterRegexOperator(self, ctx:MapCSSParser.RegexOperatorContext):
        pass

    # Exit a parse tree produced by MapCSSParser#regexOperator.
    def exitRegexOperator(self, ctx:MapCSSParser.RegexOperatorContext):
        pass


    # Enter a parse tree produced by MapCSSParser#booleanExpression.
    def enterBooleanExpression(self, ctx:MapCSSParser.BooleanExpressionContext):
        pass

    # Exit a parse tree produced by MapCSSParser#booleanExpression.
    def exitBooleanExpression(self, ctx:MapCSSParser.BooleanExpressionContext):
        pass


    # Enter a parse tree produced by MapCSSParser#valueExpression.
    def enterValueExpression(self, ctx:MapCSSParser.ValueExpressionContext):
        pass

    # Exit a parse tree produced by MapCSSParser#valueExpression.
    def exitValueExpression(self, ctx:MapCSSParser.ValueExpressionContext):
        pass


    # Enter a parse tree produced by MapCSSParser#regexExpression.
    def enterRegexExpression(self, ctx:MapCSSParser.RegexExpressionContext):
        pass

    # Exit a parse tree produced by MapCSSParser#regexExpression.
    def exitRegexExpression(self, ctx:MapCSSParser.RegexExpressionContext):
        pass


    # Enter a parse tree produced by MapCSSParser#functionExpression.
    def enterFunctionExpression(self, ctx:MapCSSParser.FunctionExpressionContext):
        pass

    # Exit a parse tree produced by MapCSSParser#functionExpression.
    def exitFunctionExpression(self, ctx:MapCSSParser.FunctionExpressionContext):
        pass


    # Enter a parse tree produced by MapCSSParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:MapCSSParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by MapCSSParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:MapCSSParser.PrimaryExpressionContext):
        pass


